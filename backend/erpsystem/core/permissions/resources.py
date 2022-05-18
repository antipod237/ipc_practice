from starlette.responses import JSONResponse

from erpsystem.core.utils import jwt_required
from erpsystem.core.models import PermissionModel


@jwt_required
async def get_apps(request, user):
    sub = PermissionModel.alias()
    apps = await PermissionModel.outerjoin(
        sub, PermissionModel.id == sub.id
    ).select().where(
        PermissionModel.role_id == user.role_id
    ).gino.load(
        PermissionModel.distinct(PermissionModel.app_name).load(
            actions=sub.action
        )
    ).all()

    result = {}
    for app in apps:
        _app = app.jsonify()
        result[_app['appName']] = _app['actions']

    return JSONResponse(result)
