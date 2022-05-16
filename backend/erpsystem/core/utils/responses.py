from starlette.responses import JSONResponse, Response


def make_error(description, status_code=400):
    return JSONResponse({
        'description': description
    }, status_code=status_code)


def make_list_response(items, total):
    return JSONResponse({
        'items': items,
        'total': total,
    })


def make_response(content, background=None):
    if background:
        return JSONResponse(content, background=background)
    return JSONResponse(content)


NO_CONTENT = Response('', status_code=204)
