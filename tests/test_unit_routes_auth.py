import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from routes.auth import signup, login, confirmed_email, refresh_token, request_email

class TestRoutsAuth(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1)

    async def test_signup(self):
        pass


    async def test_signup_failed(self):
        pass

    async def test_login_failed(self):
        pass

    async def test_login(self):
        pass

    async def test_confirmed_email(self):
        pass

    async def test_confirmed_email_failed(self):
        pass

    async def test_refresh_token(self):
        pass

    async def test_refresh_token_failed(self):
        pass

    async def test_request_email(self):
        pass

    async def test_request_email_failed(self):
        pass



if __name__ == '__main__':
    unittest.main()