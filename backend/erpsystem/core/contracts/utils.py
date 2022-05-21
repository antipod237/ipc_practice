from ..models import SupplierModel


async def is_supplier_exists(supplier_id, *args):
    supplier = await SupplierModel.get(supplier_id)
    if supplier:
        return True
    return False