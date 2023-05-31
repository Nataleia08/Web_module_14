from unittest.mock import MagicMock, patch, AsyncMock, Mock
from database.models import User, Contact
from services.auth import auth_service
import pytest




# @pytest.fixture()
# def token(client, user, session, monkeypatch):
#     # mock_send_email = MagicMock()
#     # monkeypatch.setattr("routes.auth.send_email", mock_send_email)
#     client.post("/api/auth/signup", json=user)
#     current_user: User = session.query(User).filter(User.email == user.get('email')).first()
#     # current_user.confirmed_email = True
#     # session.commit()
#     response = client.post(
#         "/api/auth/login",
#         data={"username": user.get('email'), "password": user.get('password')},
#     )
#     data = response.json()
#     return data["access_token"]


def test_send_email(client, user, session, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.set
        response = client.post("/api/request_email", json={"email": "nataleia.orlovska@gmail.com"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["message"] == "Check your email for confirmation."

def test_confirmed_email(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get(
            "/confirmed_email/{token}", token)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["message"] == "Email confirmed"


if __name__ == "__main__":
    pytest.main()