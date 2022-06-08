from ..database import db


class SalesModel(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    store_item_id = db.Column(
        db.Integer, db.ForeignKey('store_items.id'), nullable=False
    )
    value = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date(), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._store_items = set()

    @property
    def store_items(self):
        return self._store_items

    @store_items.setter
    def store_item(self, value):
        self._store_items.add(value)

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'store_item_id': self.store_item_id,
            'value': self.value,
            'date': self.date.isoformat()
        }

        if for_card:
            result['store_items'] = [
                {
                    'store_item_id': store_item.id,
                    'name': store_item.name,
                    'value': store_item.value
                }
                for store_item in self.store_items
            ]

        return result
