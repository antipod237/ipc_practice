from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from .utils import is_value_fit_in, update_store_items

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_response,
    make_list_response, validation, make_error,
    Permissions, GinoQueryHelper, NO_CONTENT, get_date
)
from ..models import (
    PurchaseModel, ItemSetModel,
    UserModel, StoreItemsModel,
    PermissionAction
)

permissions = Permissions(app_name='purchases')


class Purchases(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'item_set_id': {
            'required': True,
            'type': int
        },
        'value': {
            'required': True,
            'type': int
        },
        'date': {
            'required': True,
            'type': str
        },
        'store_item_id': {
            'required': True,
            'type': int
        },
        'user_id': {
            'required': True,
            'type': int
        },
        'is_complete': {
            'required': False,
            'type': bool
        }
    })
    async def post(self, data):
        if await is_value_fit_in(data['value'], data['store_item_id']):
            purchase = await PurchaseModel.create(
                item_set_id=data['item_set_id'],
                value=data['value'],
                date=get_date(data['date']),
                store_item_id=data['store_item_id'],
                user_id=data['user_id'],
                is_complete=data['is_complete']
            )
            if data['is_complete']:
                await update_store_items(data['value'], data['store_item_id'])
            return make_response({'id': purchase.id})

        exeption_value = data['value']
        return make_error(
            f'Невозможно добавить {exeption_value}, '
            f'сделайте колличество меньше',
            status_code=400
        )

    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = PurchaseModel.query
        total_query = db.select([db.func.count(PurchaseModel.id)])

        if 'item_set_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                PurchaseModel.item_set_id,
                int(query_params['item_set_id']),
                current_query,
                total_query
            )
        if 'store_item_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                PurchaseModel.store_item_id,
                int(query_params['store_item_id']),
                current_query,
                total_query
            )

        if 'user_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                PurchaseModel.user_id,
                int(query_params['user_id']),
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': PurchaseModel.id,
                'value': PurchaseModel.value,
                'date': PurchaseModel.date
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )


class Purchase(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        purchase_id = request.path_params['id']
        current_query = (
            PurchaseModel
            .outerjoin(UserModel)
            .outerjoin(ItemSetModel)
            .outerjoin(StoreItemsModel)
            .select()
        ).where(
            PurchaseModel.id == purchase_id
        )

        purchases = await current_query.gino.load(
            PurchaseModel.distinct(PurchaseModel.id).load(
                user=UserModel,
                item_set=ItemSetModel,
                store_item=StoreItemsModel
            )
        ).all()

        if purchases:
            return make_response(purchases[0].jsonify(for_card=True))
        return make_error(description='Purchase not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'item_set_id': {
            'required': True,
            'type': int
        },
        'value': {
            'required': True,
            'type': int
        },
        'date': {
            'required': True,
            'type': str
        },
        'store_item_id': {
            'required': True,
            'type': int
        },
        'user_id': {
            'required': True,
            'type': int
        },
        'is_complete': {
            'required': False,
            'type': bool
        }
    }, return_request=True)
    async def patch(self, request, data):
        purchase_id = request.path_params['id']
        purchase = await PurchaseModel.get(purchase_id)
        try:
            if not purchase:
                return make_error(
                    f'Purchase with id {purchase_id} not found',
                    status_code=404
                )
            if await is_value_fit_in(data['value'], data['store_item_id']):
                values = {
                    'item_set_id': data['item_set_id']
                    if 'item_set_id' in data else None,
                    'value': data['value']
                    if 'value' in data else None,
                    'date': get_date(data['date'])
                    if 'date' in data else None,
                    'store_item_id': data['store_item_id']
                    if 'store_item_id' in data else None,
                    'user_id': data['user_id']
                    if 'user_id' in data else None,
                    'is_complete': data['is_complete']
                    if 'is_complete' in data else None,
                }

                if data['is_complete']:
                    await update_store_items(
                        data['value'], data['store_item_id']
                    )

                await purchase.update(**values).apply()
                return NO_CONTENT

            exeption_value = data['value']
            return make_error(
                f'Невозможно добавить {exeption_value}, '
                f'сделайте колличество меньше',
                status_code=400
            )

        except Exception as exeption:
            return make_error(
                exeption.args[0],
                status_code=400
            )


routes = [
    Route('/', Purchases),
    Route('/{id:int}', Purchase),
]
