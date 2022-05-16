from .. import db
from . import make_error
from ..models import RoleModel, PermissionModel, PermissionAction


class Permissions:
    def __init__(self, app_name):
        self.app_name = app_name

    def required(
            self, action, *arguments, return_role=False, return_user=False
    ):
        def wrapper(func):
            async def wrapper_view(*args, user, **kwargs):
                if not user:
                    raise ValueError('User not in arguments!!!')
                role = await RoleModel.get(user.role_id)
                if not role:
                    return make_error(
                        "User doesn't have a role", status_code=403
                    )
                permission = await PermissionModel.query.where(
                    (PermissionModel.app_name == self.app_name)
                    & (PermissionModel.role_id == role.id)
                    & (
                        (PermissionModel.action == action)
                        | (PermissionModel.action == PermissionAction.ALL)
                    )
                ).gino.first()

                if not permission:
                    return make_error(
                        "Forbidden", status_code=403
                    )

                results = {}
                if return_user:
                    results['user'] = user
                if return_role:
                    results['role'] = role
                return await func(*args, **results, **kwargs)

            return wrapper_view

        if len(arguments) > 0:
            return wrapper(arguments[0])
        return wrapper

    async def get_actions(self, role_id):
        actions = await db.select([
            PermissionModel.action
        ]).select_from(
            PermissionModel
        ).where(
            (PermissionModel.app_name == self.app_name)
            & (PermissionModel.role_id == role_id)
        ).gino.all()
        return {
            'actions': [action[0] for action in actions]
        }
