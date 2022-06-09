from ..database import db
from ..models import ContractItemSetModel


async def change_contracts(contracts, item_set_id, is_create=False):
    contract_ids = [contract['contract_id'] for contract in contracts]

    if len(contracts) == 0:
        await ContractItemSetModel.delete.where(
            ContractItemSetModel.item_set_id == item_set_id
        ).gino.status()
    else:
        contracts_exist = await ContractItemSetModel.query.where(
            (ContractItemSetModel.item_set_id == item_set_id)
            & (ContractItemSetModel.contract_id.in_(contract_ids))
        ).gino.all()

        count = await db.select(
            [db.func.count(ContractItemSetModel.contract_id)]
        ).where(
            ContractItemSetModel.item_set_id == item_set_id
        ).gino.scalar()

        if len(contracts_exist) != len(contracts) or count != len(contracts):
            if not is_create:
                await ContractItemSetModel.delete.where(
                    (ContractItemSetModel.item_set_id == item_set_id) &
                    ~ (ContractItemSetModel.contract_id.in_(contract_ids))
                ).gino.status()

            models_ids = [model.contract_id for model in contracts_exist]

            result = []

            for contract in contracts:
                if contract["contract_id"] not in models_ids:
                    result.append({
                        'item_set_id': item_set_id,
                        'contract_id': contract['contract_id']
                    })

            if result:
                await ContractItemSetModel.insert().gino.all(result)
