from ..models import StoreItemsModel


async def is_value_fit_in(value, store_item_id):
    store_item = await StoreItemsModel.query.where(
        (StoreItemsModel.id == store_item_id)
    ).gino.first()
    check_value = store_item.max_value - store_item.value - value
    if check_value >= 0:
        return True
    return False


async def update_store_items(new_value, store_item_id):
    store_item = await StoreItemsModel.query.where(
        (StoreItemsModel.id == store_item_id)
    ).gino.first()
    if is_value_fit_in(new_value, store_item_id):
        updated_value = store_item.value + new_value

        await store_item.update(value=updated_value).apply()
