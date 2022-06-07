from ..database import db


class PurchaseModel(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    item_set_id = db.Column(
        db.Integer, db.ForeignKey('item_sets.id'), nullable=False
    )
    value = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date(), nullable=False)
    store_item_id = db.Column(
        db.Integer, db.ForeignKey('store_items.id'), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    is_complete = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._item_sets = None
        self._users = None
        self._store_items = None

    @property
    def item_sets(self):
        return self._item_sets

    @property
    def store_items(self):
        return self._store_items

    @property
    def users(self):
        return self._users

    @item_sets.setter
    def item_set(self, value):
        self._item_set = value

    @users.setter
    def user(self, value):
        self._user = value

    @store_items.setter
    def store_item(self, value):
        self._store_items = value

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'item_set_id': self.item_set_id,
            'store_item_id': self.store_item_id,
            'date': self.date.isoformat(),
            'is_complete': self.is_complete
        }

        if for_card:
            result['item_set'] = [
                {
                    'item_set_id': item_set.id,
                    'name': item_set.name
                }
                for item_set in self.item_set
            ]
            result['store_item'] = [
                {
                    'store_item_id': store_item.id,
                    'name': store_item.name,
                }
                for store_item in self.store_items
            ]
            result['user'] = [
                {
                    'user_id': user.id,
                    'username': user.display_name,
                }
                for user in self.users
            ]

        return result
