from ..database import db


class SupplierModel(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)

    def jsonify(self, for_card=True):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
        }

    @classmethod
    async def get_by_identifier(cls, identifier):
        return await cls.query.where(
            (cls.id == identifier)
        ).gino.first()
