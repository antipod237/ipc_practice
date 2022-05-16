from functools import wraps
from starlette.responses import Response


def with_transaction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        connection = args[1].get('connection')

        # Offline mode
        if not connection:
            print('Warning! Offline mode!')
            return await func(*args, **kwargs)

        tx = await connection.transaction()

        try:
            result = await func(*args, **kwargs)

            # Workaround for an inability to move `serializer_middleware` to
            # the start of middlewares: attempt to get status and
            # response from result as tuple or standalone object.
            status = 200
            commit_anyway = False

            if isinstance(result, tuple) and len(result) > 1:
                status = result[1]
            elif isinstance(result, Response):
                status = result.status_code
                if hasattr(result, 'commit_anyway'):
                    commit_anyway = result.commit_anyway

            if commit_anyway or (199 < status < 400):
                await tx.commit()
            else:
                await tx.rollback()
            return result
        except Exception:
            await tx.rollback()
            raise
    return wrapper
