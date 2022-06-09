from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from .utils import is_value_correct, store_items_update

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_response,
    make_list_response, validation, make_error,
    Permissions, GinoQueryHelper, NO_CONTENT, get_date,
    check_positive_value
)
from ..models import (
    SalesModel, StoreItemsModel,
    PermissionAction
)

permissions = Permissions(app_name='sales')


class Sales(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'store_item_id': {
            'required': True,
            'type': int
        },
        'value': {
            'required': True,
            'type': int,
            'value': True
        },
        'date': {
            'required': True,
            'type': str
        }
    }, custom_checks={
        'value': {
            'func': lambda v, *args: check_positive_value(v),
            'message': lambda v, *args: f'`{v}` не является корректным'
            f' количеством, сделайте его положительным'
        }
    })
    async def post(self, data):
        if await is_value_correct(data['store_item_id'], data['value']):
            sale = await SalesModel.create(
                store_item_id=data['store_item_id'],
                value=data['value'],
                date=get_date(data['date'])
            )
            await store_items_update(data['store_item_id'], data['value'])
            return make_response({'id': sale.id})

        exeption_value = data['value']
        return make_error(
            f'Невозможно продать {exeption_value}, '
            f'впишите иное количество',
            status_code=400
        )

    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = SalesModel.query
        total_query = db.select([db.func.count(SalesModel.id)])

        if 'store_item_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                SalesModel.store_item_id,
                int(query_params['store_item_id']),
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': SalesModel.id,
                'value': SalesModel.value,
                'date': SalesModel.date
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )


class Sale(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        sale_id = request.path_params['id']
        current_query = (
            SalesModel
            .outerjoin(StoreItemsModel)
            .select()
        ).where(
            SalesModel.id == sale_id
        )

        sales = await current_query.gino.load(
            SalesModel.distinct(SalesModel.id).load(
                store_item=StoreItemsModel
            )
        ).all()

        if sales:
            return make_response(sales[0].jsonify(for_card=True))
        return make_error(description='Sale not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'store_item_id': {
            'required': True,
            'type': int
        },
        'value': {
            'required': True,
            'type': int,
            'value': True
        },
        'date': {
            'required': True,
            'type': str
        }
    }, custom_checks={
        'value': {
            'func': lambda v, *args: check_positive_value(v),
            'message': lambda v, *args: f'`{v}` не является корректным'
            f' количеством, сделайте его положительным'
        }
    }, return_request=True)
    async def patch(self, request, data):
        sale_id = request.path_params['id']
        sale = await SalesModel.get(sale_id)
        try:
            if not sale:
                return make_error(
                    f'Sale with id {sale_id} not found',
                    status_code=404
                )
            if await is_value_correct(data['store_item_id'], data['value']):
                values = {
                    'store_item_id': data['store_item_id']
                    if 'store_item_id' in data else None,
                    'value': data['value']
                    if 'value' in data else None,
                    'date': get_date(data['date'])
                    if 'date' in data else None,
                }

                await store_items_update(
                    data['store_item_id'], data['value']
                )

                await sale.update(**values).apply()
                return NO_CONTENT

            exeption_value = data['value']
            return make_error(
                f'Невозможно продать {exeption_value}, '
                f'впишите иное количество',
                status_code=400
            )

        except Exception as exeption:
            return make_error(
                exeption.args[0],
                status_code=400
            )


routes = [
    Route('/', Sales),
    Route('/{id:int}', Sale),
]
