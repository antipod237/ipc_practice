from ..database import db


class ItemSetModel(db.Model):
    __tablename__ = 'item_sets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._contracts = set()

    @property
    def contracts(self):
        return self._contracts

    @contracts.setter
    def contracts(self, value):
        self._contracts.add(value)

    def jsonify(self, for_card=True):
        result = {
            'id': self.id,
            'name': self.name,
        }

        return result


class ContractItemSetModel(db.Model):
    __tablename__ = 'contracts_item_sets'

    contract_id = db.Column(
        db.Integer, db.ForeignKey('contracts.id'), nullable=False
    )
    item_set_id = db.Column(
        db.Integer, db.ForeignKey('item_sets.id'), nullable=False
    )

    def jsonify(self):
        result = {
            'contract_id': self.contract_id,
            'item_set_id': self.item_set_id,
        }

        return result
