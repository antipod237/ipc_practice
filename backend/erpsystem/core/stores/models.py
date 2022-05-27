from erpsystem.core.database import db


class StoresModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def jsonify(self, for_card=True):
        return {
            'id': self.id,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
        }
