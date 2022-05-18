from erpsystem.core.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    deactivated = db.Column(db.Boolean, nullable=False, default=False)
    display_name = db.Column(db.String(50), nullable=False)
    path_to_image = db.Column(db.String(120))
    session = db.Column(db.String(36), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'displayName': self.display_name,
            'roleId': self.role_id
        }

        if for_card:
            result['username'] = self.username
            result['email'] = self.email
            result['deactivated'] = self.deactivated

        return result

    @classmethod
    async def get_by_identifier(cls, identifier):
        return await cls.query.where(
            (cls.email == identifier) | (cls.username == identifier)
        ).gino.first()
