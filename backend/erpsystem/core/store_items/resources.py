from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_error,
    validation, GinoQueryHelper, Permissions,
    make_list_response, make_response, NO_CONTENT,
    get_one,
)
from ..models import StoreItemsModel, PermissionAction
from .utils import (
    is_store_exists, is_value_fit_in,
    is_store_item_exists, is_value_correct
)

permissions = Permissions(app_name='store_items')


class StoreItems(HTTPEndpoint):

    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = StoreItemsModel.query
        total_query = db.select([db.func.count(StoreItemsModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                StoreItemsModel.id,
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
                'id': StoreItemsModel.id,
                'name': StoreItemsModel.name,
                'value': StoreItemsModel.value,
                'max_value': StoreItemsModel.max_value,
                'store_id': StoreItemsModel.store_id,
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total,
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'name': {
            'required': True,
            'type': str,
            'max_length': 100,
            'name': True
        },
        'value': {
            'required': False,
            'type': int,
            'value': True
        },
        'max_value': {
            'required': True,
            'type': int
        },
        'store_id': {
            'required': True,
            'type': int,
            'store_id': True
        },
    }, custom_checks={
        'name': {
            'func': lambda z, *args: is_store_item_exists(z),
            'message': lambda z, *args: f'Товар с `name` `{z}`'
            f' уже существует.'
        },
        'store_id': {
            'func': lambda v, *args: is_store_exists(v),
            'message': lambda v, *args: f'Магазин с `id` `{v}`'
            f' не существует.'
        },
        'value': {
            'func': lambda z, *args: is_value_correct(z),
            'message': lambda z, *args: f'`{z}` не является корректным'
            f' количеством, сделайте его не отрицательным'
        }
    })
    async def post(self, data):
        if await is_value_fit_in(data['value'], data['max_value']):
            new_store_item = await StoreItemsModel.create(
                name=data['name'],
                value=data['value'],
                max_value=data['max_value'],
                store_id=data['store_id'],
            )
            return make_response({'id': new_store_item.id})

        exeption_value = data['value']
        return make_error(
            f'Невозможно добавить {exeption_value}, '
            f'впишите иное количество',
            status_code=400
        )


class StoreItem(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            StoreItemsModel,
            request.path_params['id'],
            'Товар'
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'name': {
            'required': True,
            'type': str,
            'max_length': 100
        },
        'value': {
            'required': False,
            'type': int,
            'value': True
        },
        'max_value': {
            'required': True,
            'type': int
        },
        'store_id': {
            'required': True,
            'type': int,
            'store_id': True
        },
        }, custom_checks={
            'store_id': {
                'func': lambda v, *args: is_store_exists(v),
                'message': lambda v, *args: f'Магащин с `id` `{v}`'
                f' не существует.'
            },
            'value': {
                'func': lambda z, *args: is_value_correct(z),
                'message': lambda z, *args: f'`{z}` не является корректным'
                f' количеством, сделайте его не отрицательным'
            }
    }, return_request=True)
    async def patch(self, request, data):
        store_item_id = request.path_params['id']
        store_item = await StoreItemsModel.get(store_item_id)
        if not store_item:
            return make_error(
                f'Магазин с идентификатором {store_item_id} не найден',
                status_code=404
            )
        if await is_value_fit_in(data['value'], data['max_value']):
            values = {
                'name': data['name']
                if 'name' in data else None,
                'value': data['value']
                if 'value' in data else None,
                'max_value': data['max_value']
                if 'max_value' in data else None,
                'store_id': data['store_id']
                if 'store_id' in data else None,
            }

            values = dict(filter(
                lambda item: item[1] is not None, values.items()
                ))

            await store_item.update(**values).apply()

            return NO_CONTENT

        exeption_value = data['value']
        return make_error(
            f'Невозможно добавить {exeption_value}, '
            f'впишите иное количество',
            status_code=400
        )


routes = [
    Route('/', StoreItems),
    Route('/{id:int}', StoreItem),
]
