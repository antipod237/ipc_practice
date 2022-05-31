from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_error,
    validation, GinoQueryHelper, Permissions,
    make_list_response, make_response, NO_CONTENT,
)
from ..models import ItemSetModel, ContractItemSetModel
from ..models import PermissionAction
from .utils import change_contracts

permissions = Permissions(app_name='item_sets')


class ItemSets(HTTPEndpoint):

    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        query_params = request.query_params

        current_query = (
            ItemSetModel
            .outerjoin(ContractItemSetModel)
            .select()
        )
        total_query = db.select([db.func.count(ItemSetModel.id)])

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                ItemSetModel.id,
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
                'id': ItemSetModel.id,
                'name': ItemSetModel.name,
            }
        )
        total = await total_query.gino.scalar()
        items = await current_query.gino.load(
            ItemSetModel.distinct(ItemSetModel.id).load(
                contracts=ContractItemSetModel
            )
        ).all()

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
            'min_length': 4,
            'max_length': 100,
        },
        'contracts': {
            'required': False
        }
    })
    async def post(self, data):
        try:
            item_set = await ItemSetModel.create(
                name=data['name'],
            )

            if 'contracts' in data:
                await change_contracts(data['contracts'], item_set.id, True)

            return make_response({'id': item_set.id})
        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )


class ItemSet(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        item_set_id = request.path_params['id']
        current_query = (
            ItemSetModel
            .outerjoin(ContractItemSetModel)
            .select()
        ).where(
            ItemSetModel.id == item_set_id
        )

        item_sets = await current_query.gino.load(
            ItemSetModel.distinct(ItemSetModel.id).load(
                contracts=ContractItemSetModel
            )
        ).all()

        if item_sets:
            return make_response(item_sets[0].jsonify(for_card=True))
        return make_error(description='Item set not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'name': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 100,
        }
    }, return_request=True)
    async def patch(self, request, data):
        item_set_id = request.path_params['id']
        item_set = await ItemSetModel.get(item_set_id)
        try:
            if not item_set:
                return make_error(
                    f'Item set with id {item_set_id} not found',
                    status_code=404
                )

            values = {
                'name': data['name'] if 'name' in data else None
            }

            await item_set.update(**values).apply()

            if 'contracts' in data:
                await change_contracts(data['contracts'], item_set_id)

        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

        return NO_CONTENT


routes = [
    Route('/', ItemSets),
    Route('/{id:int}', ItemSet),
]
