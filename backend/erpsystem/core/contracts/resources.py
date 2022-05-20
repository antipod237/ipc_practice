import json
from datetime import date
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..models import ContractModel, PermissionAction
from ..utils import (
    with_transaction, jwt_required, make_error,
    validation, GinoQueryHelper, Permissions,
    make_list_response, make_response, NO_CONTENT, get_one,
)

permissions = Permissions(app_name='contracts')


class Contracts(HTTPEndpoint):
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(self, request):
        data = request.query_params
        contracts_query = ContractModel.query
        total_query = db.select([db.func.count(ContractModel.id)])

        if 'id' in data:
            ids = json.loads(data['id'])
            current_query, total_query = GinoQueryHelper.in_(
                contracts_query,
                total_query,
                ContractModel.id,
                ids
            )

        if 'number' in data:
            contracts_query, total_query = GinoQueryHelper.search(
                ContractModel.number,
                data['number'],
                contracts_query,
                total_query
            )

        if 'start_date' in data:
            year, month, day = data['start_date'].split('-')[:3]
            contracts_query = contracts_query.where(
                ContractModel.start_date >= date(year, month, day)
            )
            total_query = total_query.where(
                ContractModel.start_date >= date(year, month, day)
            )
        if 'end_date' in data:
            year, month, day = data['end_date'].split('-')[:3]
            contracts_query = contracts_query.where(
                ContractModel.start_date <= date(year, month, day)
            )
            total_query = total_query.where(
                ContractModel.start_date <= date(year, month, day)
            )

        if 'supplier_id' in data:
            # TODO replace with equal
            contracts_query = contracts_query.where(
                ContractModel.provider_id == int(data['supplier_id'])
            )
            total_query = total_query.where(
                ContractModel.provider_id == int(data['supplier_id'])
            )

        contracts_query = GinoQueryHelper.pagination(
            data, contracts_query
        )

        contracts_query = GinoQueryHelper.order(
            data,
            contracts_query,
            {
                'id': ContractModel.id,
                'number': ContractModel.number,
                'start_date': ContractModel.start_date,
                'end_date': ContractModel.end_date,
                'supplier_id': ContractModel.supplier_id,
            }
        )

        contracts = await contracts_query.gino.all()

        return make_list_response(
            [contract.jsonify() for contract in contracts],
            total=await total_query.gino.scalar()
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    async def post(self, request):

        data = await request.json()

        number = data['number']
        start_date = self._get_date(data['start_date'])
        end_date = self._get_date(data['end_date'])
        supplier_id = data['supplier_id']

        contract = await ContractModel.create(
            number=number,
            start_date=start_date,
            end_date=end_date,
            supplier_id=supplier_id,
        )

        return make_response({'id': contract.id})

    @staticmethod
    def _get_date(text_date):
        year, month, day = [int(i) for i in text_date.split('-')]
        return date(year, month, day)


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
            'type': str,
            'min_length': 1,
            'max_length': 50,
        },
        'start_date': {
            'type': date,
        },
        'end_date': {
            'type': date,
        },
        'supplier_id': {
            'type': int,
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
            'start_date': data['start_date']
            if 'start_date' in data else None,
            'end_date': data['end_date']
            if 'end_date' in data else None,
            'supplier_id': data['supplier_id']
            if 'supplier_id' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await contract.update(**values).apply()

        return NO_CONTENT

routes = [
    Route('/', Contracts),
    Route('/{contract_id:int}', Contract),
]
