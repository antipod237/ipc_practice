from validate_email import validate_email

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_error,
    validation, GinoQueryHelper, Permissions,
    make_list_response, make_response, NO_CONTENT, get_one,
)
from ..models import StoresModel, PermissionAction

permissions = Permissions(app_name='stores')


class Stores(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = StoresModel.query
        total_query = db.select([db.func.count(StoresModel.id)])

        query_params = request.query_params

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': StoresModel.id,
                'address': StoresModel.address,
                'phone_number': StoresModel.phone_number,
                'email': StoresModel.email,
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
        'address': {
            'required': True,
            'type': str,
        },
        'phone_number': {
            'required': True,
            'type': str,
        },
        'email': {
            'required': True,
            'type': str,
            'email': True,
        },
    }, custom_checks={
        'email': {
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
    })
    async def post(self, data):
        new_store = await StoresModel.create(
            address=data['address'],
            phone_number=data['phone_number'],
            email=data['email'],
        )
        return make_response({'id': new_store.id})


class Store(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            StoresModel,
            request.path_params['id'],
            'Магазин'
        )

    # TODO: make this method for admin only

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'address': {
            'type': str,
        },
        'phone_number': {
            'type': str,
        },
        'email': {
            'type': str,
            'email': True,
        },
    }, custom_checks={
        'email': {
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
    }, return_request=True)
    async def patch(self, request, data):
        store_id = request.path_params['id']
        store = await StoresModel.get(store_id)
        if not store:
            return make_error(
                f'Магазин с идентификатором {store_id} не найден',
                status_code=404
            )

        values = {
            'address': data['address']
            if 'address' in data else None,
            'phone_number': data['phone_number']
            if 'phone_number' in data else None,
            'email': data['email']
            if 'email' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await store.update(**values).apply()

        return NO_CONTENT


routes = [
    Route('/', Stores),
    Route('/{id:int}', Store),
]
