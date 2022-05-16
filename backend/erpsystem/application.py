from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['POST', 'GET', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['*']
    )
]


def create_app():
    from . import db
    from .core import routes
    app = Starlette(
        debug=True,
        routes=[Mount('/api', routes=routes)],
        middleware=middleware
    )

    from .config import TESTING

    if not TESTING:
        db.init_app(app)
    return app
