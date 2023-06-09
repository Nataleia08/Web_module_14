from unittest.mock import MagicMock, patch, AsyncMock, Mock
from database.models import User, Contact
from services.auth import auth_service
import pytest




@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    # assert response.status_code == 201, response.text
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed_email = True
    session.commit()
    body = {"username": user.get('email'), "password": user.get('password')}
    response = client.post("/api/auth/login", data = body, )
    assert response.status_code == 200, response.text
    data = response.json()
    return data["access_token"]


def test_create_contact(client, user, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.post(
            "/api/contacts",
            json={"email": "test@gamil.com", "first_name": "Tester", "last_name": "Testerovich", "phone_number": "+380668889900", "day_birthday": "2000-05-28"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == "test@gamil.com"
        assert data["first_name"] == "Tester"
        assert data["last_name"] == "Testerovich"
        assert data["phone_number"] == "+380668889900"
        assert data["day_birthday"] == '2000-05-28'
        assert "id" in data


def test_get_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test@gamil.com"
        assert data["first_name"] == "Tester"
        assert data["last_name"] == "Testerovich"
        assert data["phone_number"] == "+380668889900"
        assert data["day_birthday"] == '2000-05-28'
        assert "id" in data


def test_get_contact_not_found(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found"


def test_get_contacts(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["email"] == "test@gamil.com"
        assert data[0]["first_name"] == "Tester"
        assert data[0]["last_name"] == "Testerovich"
        assert data[0]["phone_number"] == "+380668889900"
        assert data[0]["day_birthday"] == '2000-05-28'
        assert "id" in data[0]


def test_update_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.put(
            "/api/contacts/1",
            json={"email": "test1@gamil.com", "first_name": "Bob", "last_name": "Smit", "phone_number": "+380668889000", "day_birthday": "2000-05-26"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test1@gamil.com"
        assert data["first_name"] == "Bob"
        assert data["last_name"] == "Smit"
        assert data["phone_number"] == "+380668889000"
        assert data["day_birthday"] == '2000-05-26'
        assert "id" in data


def test_update_contact_not_found(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.put(
            "/api/contacts/2",
            json={"email": "test2@gamil.com", "first_name": "Bob", "last_name": "Smit", "phone_number": "+380668889000", "day_birthday": "2000-05-26"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found"


def test_delete_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text


def test_repeat_delete_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found"


if __name__ == "__main__":
    pytest.main()