from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_error,
    validation, GinoQueryHelper, Permissions,
    make_list_response, make_response, NO_CONTENT,
    get_one, get_date,
)
from ..models import ContractModel, PermissionAction
from .utils import is_supplier_exists

permissions = Permissions(app_name='contracts')


class Contracts(HTTPEndpoint):

    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = ContractModel.query
        total_query = db.select([db.func.count(ContractModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                ContractModel.number,
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
                'id': ContractModel.id,
                'number': ContractModel.number,
                'start_date': ContractModel.start_date,
                'end_date':  ContractModel.end_date,
                'supplier_id': ContractModel.supplier_id,
            }
        )
        print(ContractModel.start_date)
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
        'number': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'start_date': {
            'required': True,
            'type': str,
        },
        'end_date': {
            'required': True,
            'type': str,
        },
        'supplier_id': {
            'required': True,
            'type': int,
            'supplier_id': True
        },
    }, custom_checks={
        'supplier_id': {
            'func': lambda v, *args: is_supplier_exists(v),
            'message': lambda v, *args: f'Поставщик с `id` `{v}` не существует.'
        }
    })
    async def post(self, data):
        new_contract = await ContractModel.create(
            number=data['number'],
            start_date=get_date(data['start_date']),
            end_date=get_date(data['end_date']),
            supplier_id=data['supplier_id'],
        )
        return make_response({'id': new_contract.id})


class Contract(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            ContractModel,
            request.path_params['id'],
            'Договор'
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'number': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'start_date': {
            'required': True,
            'type': str,
        },
        'end_date': {
            'required': True,
            'type': str,
        },
        'supplier_id': {
            'required': True,
            'type': int,
        'supplier_id': True
        }
        }, custom_checks={
            'supplier_id': {
                'func': lambda v, *args: is_supplier_exists(v),
                'message': lambda v, *args: f'Поставщик с `id` `{v}` не существует.'
            },
    }, return_request=True)
    async def patch(self, request, data):
        contract_id = request.path_params['id']
        contract = await ContractModel.get(contract_id)
        if not contract:
            return make_error(
                f'Договор с идентификатором {contract_id} не найден',
                status_code=404
            )

        values = {
            'number': data['number']
            if 'number' in data else None,
            'start_date': get_date(data['start_date'])
            if 'start_date' in data else None,
            'end_date': get_date(data['end_date'])
            if 'end_date' in data else None,
            'supplier_id': data['supplier_id']
            if 'supplier_id' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await contract.update(**values).apply()

        return NO_CONTENT


routes = [
    Route('/', Contracts),
    Route('/{id:int}', Contract),
]
