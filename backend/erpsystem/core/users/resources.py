from uuid import uuid4
from validate_email import validate_email

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from passlib.hash import pbkdf2_sha256 as sha256

from erpsystem.core.database import db
from erpsystem.core.utils import (
    with_transaction, create_refresh_token, create_access_token, jwt_required,
    make_error, Permissions, validation, GinoQueryHelper, make_list_response,
    make_response, NO_CONTENT, get_one,
)
from erpsystem.core.models import UserModel, PermissionAction
from erpsystem.core.utils import is_username_unique, validate_role

permissions = Permissions(app_name='users')


class Users(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = UserModel.query
        total_query = db.select([db.func.count(UserModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                UserModel.display_name,
                query_params['search'],
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': UserModel.id,
                'displayName': UserModel.display_name,
                'roleId': UserModel.role_id,
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'username': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 50,
            'unique_username': True
        },
        'password':  {
            'required': True,
            'type': str,
            'min_length': 5,
            'max_length': 50,
        },
        'displayName': {
            'required': True,
            'type': str,
            'min_length': 5,
            'max_length': 50,
        },
        'email': {
            'required': True,
            'type': str,
            'email': True,
        },
        'roleId': {
            'required': True,
            'type': int,
            'role': True,
        }
    }, custom_checks={
        'email': {
            # with the pyDNS, it will be better
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
        'unique_username': {
            # it works with async functions
            'func': lambda v, *args: is_username_unique(v),
            'message': lambda v, *args: f'Пользователь с `username` `{v}` уже '
            f'существует.'
        },
        'role': {
            'func': validate_role,
            'message': lambda v, *args: f'Роль с `id` `{v}` не существует.'
        },
    })
    async def post(self, data):
        new_user = await UserModel.create(
            username=data['username'],
            password=sha256.hash(data['password']),
            session=str(uuid4()),
            display_name=data['displayName'],
            email=data['email'],
            role_id=data['roleId'],
        )
        return make_response({'id': new_user.id})


class User(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            UserModel,
            request.path_params['user_id'],
            'Пользователь'
        )

    # TODO: make this method for admin only

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'password': {
            'type': str,
            'min_length': 5,
            'max_length': 30,
        },
        'displayName': {
            'type': str,
            'min_length': 5,
            'max_length': 50,
        },
        'email': {
            'type': str,
            'email': True,
        },
        'roleId': {
            'type': int,
            'role': True,
        },
        'deactivated': {
            'type': bool
        }
    }, custom_checks={
        'email': {
            # with the pyDNS, it will be better
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
        'role': {
            'func': validate_role,
            'message': lambda v, *args: f'Роль с `id` `{v}` не существует.'
        }
    }, return_request=True)
    async def patch(self, request, data):
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if not user:
            return make_error(
                f'Пользователь с идентификатором {user_id} не найден',
                status_code=404
            )

        values = {
            'display_name': data['displayName']
            if 'displayName' in data else None,
            'password': sha256.hash(data['password'])
            if 'password' in data else None,
            'deactivated': data['deactivated']
            if 'deactivated' in data else None,
            'email': data['email'] if 'email' in data else None,
            'role_id': data['roleId'] if 'roleId' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await user.update(**values).apply()

        return NO_CONTENT


@validation(schema={
    'identifier': {
        'required': True,
        'type': str,
        'min_length': 4,
        'max_length': 50,
    },
    'password': {
        'required': True,
        'type': str,
        'min_length': 4,
        'max_length': 50,
    },
})
async def get_refresh_token(data):
    user = await UserModel.get_by_identifier(data['identifier'])

    if not user:
        return make_error(
            'Пользователь с таким именем или электронной почтой не найден',
            status_code=404
        )

    if not sha256.verify(data['password'], user.password):
        return make_error('Пароль неверен', status_code=401)

    return make_response({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'refresh_token': create_refresh_token(user.session),
        'access_token': create_access_token(user.session)
    })


@jwt_required(token_type='refresh')
async def get_access_token(request, user):
    return make_response({
        'access_token': create_access_token(user.session),
    })


@jwt_required
@validation(schema={
    'password': {
        'required': True,
        'type': str,
        'min_length': 4,
        'max_length': 50,
    },
})
async def reset_session(data, user):
    if not sha256.verify(data['password'], user.password):
        return make_error('Пароль неверен', status_code=401)

    await user.update(
        session=str(uuid4())
    ).apply()

    return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Users),
    Route('/{user_id:int}', User),
    Route('/actions', get_actions, methods=['GET']),
    Route('/reset-session', reset_session, methods=['POST']),
    Route('/access-tokens', get_access_token, methods=['POST']),
    Route('/refresh-tokens', get_refresh_token, methods=['POST']),
]
