from unittest.mock import MagicMock, patch, AsyncMock, Mock
from database.models import User, Contact
from services.auth import auth_service
import pytest




@pytest.fixture()
def token(client, current_user, session, monkeypatch):
    response = client.post(
        "/api/auth/login",
        data={"username": current_user.get('email'), "password": current_user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_send_email(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())

        response = client.post(
            "/api/request_email",
            json={"email": "test@gamil.com", "first_name": "Tester", "last_name": "Testerovich", "phone_number": "+380668889900", "day_birthday": "2000-05-28"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == "test@gamil.com"
        assert "id" in data

def test_confirmed_email(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.post(
            "/confirmed_email/{token}",
            json={"email": "test@gamil.com", "first_name": "Tester", "last_name": "Testerovich", "phone_number": "+380668889900", "day_birthday": "2000-05-28"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == "test@gamil.com"
        assert "id" in data