from ..database import db


class StoreItemsModel(db.Model):
    __tablename__ = 'store_items'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(
        db.Integer, db.ForeignKey('purchases.id'), nullable=False
    )
    value = db.Column(db.Integer, nullable=False)
    max_value = db.Column(db.Integer, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey('stores.id'), nullable=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._purchases = None

    @property
    def purchases(self):
        return self._purchases

    @purchases.setter
    def purchase(self, value):
        self._purchase = value

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'purchase_id': self.purchase_id,
            'value': self.value,
            'max_value': self.max_value,
            'store_id': self.store_id,
        }

        result['remaining_space'] = self.max_value - self.value

        if for_card:
            result['purchases'] = [
                {
                    'id': purchase.id,
                    'value': purchase.value,
                    'date': purchase.date
                }
                for purchase in self.purchase
            ]

        return result
