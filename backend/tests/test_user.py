from uuid import uuid4
from erpsystem.config import ADMIN_USERNAME, ADMIN_PASSWORD, TESTING, DB_URL

from tests.testconf import get_access_token, client, setup


def test_ping(client):
    response = client.get('/api/ping')

    assert response.status_code == 200, response.text


def test_tokens(client):
    response = client.post(
        '/api/users/refresh-tokens', json={
            'identifier': ADMIN_USERNAME,
            'password': ADMIN_PASSWORD
        }
    )

    assert response.status_code == 200, response.text


def test_get_users(client):
    access_token = get_access_token(client)
    response = client.get(
        '/api/users',
        headers={'Authorization':  f'Bearer {access_token}'}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data['items']) > 0


def test_create_user(client):
    access_token = get_access_token(client)
    response = client.post(
        '/api/users/',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'username': 'test_demo',
            'password': 'test_demo',
            'email': 'test@mail.com',
            'roleId': 3,
            'displayName': 'Иван Петров',
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data


def test_create_non_unique_user(client):
    access_token = get_access_token(client)
    response = client.post(
        '/api/users/',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'username': 'test_demo',
            'password': 'test_demo',
            'email': 'test@mail.com',
            'roleId': 3,
            'displayName': 'Иван Петров',
        }
    )

    assert response.status_code == 400, response.text
    data = response.json()
    assert data['description'] == (
        'Поле `username` не прошло валидацию. Ошибка: Пользователь с `username'
        '` `test_demo` уже существует.'
    )


def test_permissions(client):
    response = client.post(
        '/api/users/refresh-tokens', json={
            'identifier': 'test_demo',
            'password': 'test_demo',
        }
    )
    access_token = response.json()['access_token']

    response = client.post(
        '/api/users/',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'username': 'test_demo',
            'password': 'test_demo',
            'email': 'test@mail.com',
            'roleId': 3,
            'displayName': 'Иван Петров',
        }
    )

    assert response.status_code == 403, response.text
    data = response.json()
    assert data['description'] == 'Forbidden'


def test_user_update(client):
    access_token = get_access_token(client)
    response = client.patch(
        '/api/users/2',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'email': 'test2@mail.com',
        }
    )

    assert response.status_code == 204, response.text
