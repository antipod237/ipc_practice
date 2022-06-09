from ..models import StoreItemsModel


async def is_value_correct(store_item_id, value):
    store_item = await StoreItemsModel.query.where(
        (StoreItemsModel.id == store_item_id)
    ).gino.first()
    check_value = store_item.value - value
    if check_value >= 0:
        return True
    return False


async def store_items_update(store_item_id, value):
    store_item = await StoreItemsModel.query.where(
        (StoreItemsModel.id == store_item_id)
    ).gino.first()
    if is_value_correct(store_item_id, value):
        updated_value = store_item.value - value

        await store_item.update(value=updated_value).apply()
