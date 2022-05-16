from gino_starlette import Gino
from gino.dialects.asyncpg import AsyncEnum
from ..config import (
    DB_HOST, DB_USER, DB_DATABASE, DB_PASSWORD, DB_PORT, USE_SSL,
)


db = Gino(
    driver='postgresql',
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE,
    ssl=USE_SSL
)

db.Enum = AsyncEnum
