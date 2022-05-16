import pytest

from alembic import command
from alembic.config import Config
from starlette.testclient import TestClient

from erpsystem import create_app, db
from erpsystem.config import DB_URL, ADMIN_USERNAME, ADMIN_PASSWORD


@pytest.fixture(autouse=True)
async def setup():
    """
    Create a clean test database every time the tests are run.
    """
    async with db.with_bind(DB_URL):
        alembic_config = Config('./alembic.ini')
        command.upgrade(alembic_config, 'head')
        yield  # Run the tests.


@pytest.fixture
def client():
    """
    Make a 'client' fixture available to test cases.
    """
    # Our fixture is created within a context manager. This ensures that
    # application startup and shutdown run for every test case.
    #
    # Because we've configured the DatabaseMiddleware with
    # `rollback_on_shutdown` we'll get a complete rollback to the initial state
    # after each test case runs.
    app = create_app()
    with TestClient(app) as test_client:
        return test_client


def get_access_token(client):
    response = client.post(
        '/api/users/refresh-tokens', json={
            'identifier': ADMIN_USERNAME,
            'password': ADMIN_PASSWORD
        }
    )
    return response.json()['access_token']
