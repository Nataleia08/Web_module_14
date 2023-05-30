import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from services.auth import auth_service


class TestServicesAuth2(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1)

    async def test_create_access_token(self):
        pass

    async def test_create_refresh_token(self):
        pass

    async def test_decode_refresh_token(self):
        pass

    async def test_get_current_user(self):
        pass

    async def test_create_email_token(self):
        pass

    async def test_get_email_from_token(self):
        pass

    async def test_verify_password_failed(self):
        pass

    async def test_get_password_hash_failed(self):
        pass

    async def test_create_access_token_failed(self):
        pass

    async def test_create_refresh_token_failed(self):
        pass

    async def test_decode_refresh_token_failed(self):
        pass

    async def test_get_current_user_failed(self):
        pass

    async def test_create_email_token_failed(self):
        pass

    async def test_get_email_from_token_failed(self):
        pass



if __name__ == '__main__':
    unittest.main()