from validate_email import validate_email

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from passlib.hash import pbkdf2_sha256 as sha256

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_error, Permissions, validation, GinoQueryHelper,
    make_list_response, make_response, NO_CONTENT, get_one,
)
from ..models import SupplierModel, PermissionAction

permissions = Permissions(app_name='suppliers')


class Suppliers(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = SupplierModel.query
        total_query = db.select([db.func.count(SupplierModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                SupplierModel.name,
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
                'id': SupplierModel.id,
                'name': SupplierModel.name,
                'email': SupplierModel.email,
                'phone_number': SupplierModel.phone_number,
                'address': SupplierModel.address,
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
        'name': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'email': {
            'required': True,
            'type': str,
            'email': True,
        },
        'phone_number': {
            'required': True,
            'type': str,
        },
        'address': {
            'required': True,
            'type': str,
        },
    }, custom_checks={
        'email': {
            # with the pyDNS, it will be better
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
    })
    async def post(self, data):
        new_supplier = await SupplierModel.create(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            address=data['address'],
        )
        return make_response({'id': new_supplier.id})


class Supplier(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            SupplierModel,
            request.path_params['id'],
            'Поставщик'
        )

    # TODO: make this method for admin only

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'name': {
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'email': {
            'type': str,
            'email': True,
        },
        'phone_number': {
            'type': str,
        },
        'address': {
            'type': str,
        },
    }, 
    custom_checks={
        'email': {
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        }
    }, return_request=True)
    async def patch(self, request, data):
        supplier_id = request.path_params['id']
        supplier = await SupplierModel.get(supplier_id)
        if not supplier:
            return make_error(
                f'Поставщик с идентификатором {supplier_id} не найден',
                status_code=404
            )

        values = {
            'name': data['name']
            if 'name' in data else None,
            'email': data['email']
             if 'email' in data else None,
            'phone_number': data['phone_number']
             if 'phone_number' in data else None,
            'address': data['address']
             if 'address' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await supplier.update(**values).apply()

        return NO_CONTENT


routes = [
    Route('/', Suppliers),
    Route('/{id:int}', Supplier),
]
