import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from repository.users import birthday_in_this_year, get_user_by_email, create_user, update_token, confirmed_email, update_avatar,create_new_password

class TestDBActions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1)

    async def test_birthday_in_this_year(self):
        pass

    async def test_get_user_by_email(self):
        pass

    async def test_create_user(self):
        pass

    async def test_update_token(self):
        pass

    async def test_confirmed_email(self):
        pass

    async def test_update_avatar(self):
        pass

    async def test_create_new_password(self):
        pass


if __name__ == '__main__':
    unittest.main()