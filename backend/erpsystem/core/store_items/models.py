from ..database import db


class StoreItemsModel(db.Model):
    __tablename__ = 'store_items'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    max_value = db.Column(db.Integer, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey('stores.id'), nullable=False
    )

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'value': self.value,
            'max_value': self.max_value,
            'store_id': self.store_id,
        }

        result['remaining_space'] = self.max_value - self.value

        return result
