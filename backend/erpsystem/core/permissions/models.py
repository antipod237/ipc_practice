from erpsystem.core.database import db


class PermissionModel(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._actions = set()

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, value):
        self._actions.add(value)

    def jsonify(self):
        return {
            'appName': self.app_name,
            'actions': [action for action in self.actions],
        }


class PermissionAction:
    ALL = 'all'
    CREATE = 'create'
    UPDATE = 'update'
    GET = 'get'
