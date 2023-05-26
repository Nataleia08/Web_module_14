import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from routes.users import read_users_me, update_avatar_user, update_password

class TestRoutsUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1)

    async def test_read_users_me(self):
        pass

    async def test_update_avatar_user(self):
        pass

    async def test_update_password(self):
        pass


if __name__ == '__main__':
    unittest.main()
