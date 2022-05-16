from ..database import db


class RoleModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(64), unique=True, nullable=False)

    def jsonify(self, **kwargs):
        return {
            'id': self.id,
            'name': self.name,
            'displayName': self.display_name,
        }
