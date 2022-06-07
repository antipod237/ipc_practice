from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes
from .suppliers.resources import routes as suppliers_routes
from .contracts.resources import routes as contracts_routes
from .stores.resources import routes as stores_routes
from .itemsets.resources import routes as item_sets_routes
from .purchases.resources import routes as purchases_routes
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
    Mount('/stores', routes=stores_routes),
    Mount('/itemsets', routes=item_sets_routes),
    Mount('/purchases', routes=purchases_routes),
]
