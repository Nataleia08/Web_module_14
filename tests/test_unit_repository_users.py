import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from repository.users import birthday_in_this_year, get_user_by_email, create_user, update_token, confirmed_email, update_avatar,create_new_password
from datetime import datetime

class TestDBActions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1)

    def test_birthday_in_this_year(self):
        result = birthday_in_this_year(datetime(year=1990, month=3, day =8))
        true_result = datetime(year=2023, month=3, day =8).date()
        self.assertEqual(result, true_result)

    async def test_get_user_by_email(self):
        user_data = User()
        self.session.query().filter().first.return_value = user_data
        result = await get_user_by_email(self.user.email, db=self.session)
        self.assertEqual(user_data.email, result.email)
        self.assertEqual(user_data.confirmed_email, result.confirmed_email)
        self.assertEqual(user_data.password, result.password)
        self.assertEqual(user_data.avatar, result.avatar)
        self.assertEqual(user_data.refresh_token, result.refresh_token)
        self.assertTrue(hasattr(result, "id"))

    async def test_create_user(self):
        body = UserAuthModel(username = "tester", email= "test@gmail.com", password= "1234567")
        new_user = User(id= 2, username = "tester", email= "test@gmail.com", password= "1234567")
        self.session.query().filter().first.return_value = new_user
        result = await create_user(body=body, db=self.session)
        self.assertEqual(new_user.email, result.email)
        self.assertEqual(new_user.confirmed_email, result.confirmed_email)
        self.assertEqual(new_user.password, result.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        pass


    async def test_confirmed_email(self):
        body = UserAuthModel(username="tester", email="test@gmail.com", password="1234567")
        new_user = User(id=3, username="tester", email="test@gmail.com", password="1234567")
        self.session.query().filter().first.return_value = new_user
        result = await create_user(body=body, db=self.session)
        await confirmed_email(result, db=self.session)
        self.assertTrue(result.confirmed_email)

    async def test_update_avatar(self):
        pass

    async def test_create_new_password(self):
        pass

    async def test_get_user_by_email_failed(self):
        pass

    async def test_create_user_failed(self):
        pass

    async def test_update_token_failed(self):
        pass

    async def test_confirmed_email_failed(self):
        pass

    async def test_update_avatar_failed(self):
        pass

    async def test_create_new_password_failed(self):
        pass

if __name__ == '__main__':
    unittest.main()