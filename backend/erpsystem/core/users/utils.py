from erpsystem.core.models import RoleModel, UserModel


async def is_username_unique(username):
    user = await UserModel.query.where(
        UserModel.username == username
    ).gino.first()
    if user:
        return False
    return True


async def validate_role(role_id, *args):
    role = await RoleModel.get(role_id)
    return bool(role)
