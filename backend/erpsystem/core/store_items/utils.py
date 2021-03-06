from ..models import StoresModel, StoreItemsModel


async def is_store_exists(store_id, *args):
    store = await StoresModel.get(store_id)
    if store:
        return True
    return False


async def is_value_fit_in(value, max_value):
    check_value = max_value - value
    if check_value >= 0:
        return True
    return False


async def is_store_item_exists(name, *args):
    store_item = await StoreItemsModel.query.where(
        (StoreItemsModel.name == name)
    ).gino.all()
    if store_item:
        return False
    return True


async def is_value_correct(value):
    if value >= 0:
        return True
    return False
