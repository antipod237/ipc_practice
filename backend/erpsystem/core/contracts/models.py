from ..database import db


class ContractModel(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    number = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    supplier_id = db.Column(
        db.Integer, db.ForeignKey('suppliers.id'), nullable=True
    )

    def jsonify(self, for_card=True):
        return {
            'id': self.id,
            'number': self.number,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'supplier_id': self.supplier_id,
        }

    @classmethod
    async def get_by_identifier(cls, identifier):
        return await cls.query.where(
            (cls.id == identifier | cls.number == identifier)
        ).gino.first()
