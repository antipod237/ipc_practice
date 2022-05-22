from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes
from .suppliers.resources import routes as suppliers_routes
from .contracts.resources import routes as contracts_routes
from .permissions.resources import get_apps


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Route('/apps', get_apps, methods=['GET']),
    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
    Mount('/suppliers', routes=suppliers_routes),
    Mount('/contracts', routes=contracts_routes),
]
