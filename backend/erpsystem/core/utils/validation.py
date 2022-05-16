import inspect

from starlette.requests import Request
from json.decoder import JSONDecodeError

from . import make_error

CHECKS = {
    'type': {
        'func': lambda value, excepted_type: type(value) == excepted_type
        if type(excepted_type) is not tuple else type(value) in excepted_type,
        'message': lambda value, excepted_type: f'Поолучен тип '
        f'{type(value).__name__}, ожидался тип {excepted_type.__name__}.',
    },
    'min_length': {
        'func': lambda value, length: len(value) >= length,
        'message': lambda value, length: f'Минимальная длина поля {length}, '
        f'длинна полученного поля – {len(value)}.',
    },
    'max_length': {
        'func': lambda value, length: len(value) <= length,
        'message': lambda value, length: f'Максимальная длина поля {length}, '
        f'длинна полученного поля – {len(value)}.',
    },
    'required': {
        'func': lambda value, required: not required or bool(value),
        'message': lambda *args: 'Обязательное поле не было получено.',
    }
}


class ValidationError(Exception):
    def __init__(self, description, *args):
        super().__init__(*args)
        self.description = description


async def _validate(schema, custom_checks, data, request):
    checks = {**CHECKS}
    if custom_checks:
        checks = {**checks, **custom_checks}
    for field_name, params in schema.items():
        for param, value in params.items():
            if field_name not in data and 'required' not in params:
                continue
            if 'request' in checks[param] and checks[param]['request']:
                result = checks[param]['func'](
                    field_name in data and data[field_name], value,
                    request=request
                )
            else:
                result = checks[param]['func'](
                    field_name in data and data[field_name], value
                )
            if inspect.isawaitable(result):
                result = await result
            if not result:
                error = checks[param]['message'](
                    field_name in data and data[field_name], value
                )
                raise ValidationError(
                    f'Поле `{field_name}` не прошло валидацию. Ошибка:'
                    f' {error}'
                )


def validation(
        schema, *arguments, custom_checks=None, return_request=False,
        nullable=False
):
    def wrapper(func):
        async def wrapper_view(*args, **kwargs):
            request = list(
                filter(lambda arg: isinstance(arg, Request), args)
            )[0]
            try:
                data = await request.json()
            except JSONDecodeError:
                return make_error('Ошибка при парсинге JSON')

            if len(data) == 0 and not nullable:
                return make_error('Полее с данными пусто')

            try:
                await _validate(schema, custom_checks, data, request)
            except ValidationError as e:
                return make_error(e.description)

            result = {'data': dict(filter(
                lambda item: item[0] in schema.keys(), data.items()
            ))}

            new_args = list(
                filter(lambda v: not isinstance(v, Request), args)
            )

            if return_request:
                result['request'] = request

            return await func(*new_args, **result, **kwargs)

        return wrapper_view

    if len(arguments) > 0:
        return wrapper(arguments[0])
    return wrapper
