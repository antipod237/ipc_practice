from starlette.routing import Route
from erpsystem.core.utils import jwt_required, make_list_response, get_one
from erpsystem.core.models import RoleModel


@jwt_required(return_user=False)
async def get_roles(request):
    roles = await RoleModel.query.gino.all()
    return make_list_response(
        [role.jsonify() for role in roles],
        total=len(roles)
    )


@jwt_required(return_user=False)
async def get_role(request):
    return await get_one(RoleModel, request.path_params['role_id'], 'Роли')


routes = [
    Route('/', get_roles, methods=['GET']),
    Route('/{role_id:int}', get_role, methods=['GET']),
]
