import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from repository.users import birthday_in_this_year, get_user_by_email, create_user, update_token, confirmed_email, update_avatar, create_new_password
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
        user_data = User(refresh_token = "token")
        self.session.query().filter().first.return_value = user_data
        token = "new_token"
        await update_token(user_data, "new_token", db=self.session)
        self.assertEqual(user_data.refresh_token, token)


    async def test_confirmed_email(self):
        user_data = User(confirmed_email = False)
        self.session.query().filter().first.return_value = user_data
        await confirmed_email(user_data.email, db=self.session)
        self.assertTrue(user_data.confirmed_email)

    async def test_update_avatar(self):
        user_data = User()
        self.session.query().filter().first.return_value = user_data
        now_avatar = user_data.avatar
        await update_avatar(user_data.email, "https://www.edu.goit.global/uk/learn/7460925/10926565/12574686/textbook", db=self.session)
        self.assertNotEqual(user_data.avatar, now_avatar)

    async def test_create_new_password(self):
        user_data = User(password = "123456789")
        self.session.query().filter().first.return_value = user_data
        new_password = "000000000"
        await create_new_password(user_data.email, "000000000", db=self.session)
        self.assertEqual(user_data.password, new_password)


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