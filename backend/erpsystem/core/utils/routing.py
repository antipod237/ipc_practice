from . import make_response, make_error


async def get_one(model, entity_id, entity_name):
    user = await model.get(entity_id)
    if user:
        return make_response(user.jsonify(for_card=True))
    return make_error(
        f'{entity_name} с идентификатором {entity_id} не найден',
        status_code=404
    )
