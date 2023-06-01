import unittest
from unittest.mock import MagicMock
from fastapi import File
import cloudinary
import cloudinary.uploader

from sqlalchemy.orm import Session

from database.models import User
from routes.users import read_users_me, update_avatar_user, update_password

class TestRoutsUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, password = "00000000000")

    async def test_read_users_me(self):
        result = await read_users_me(current_user = self.user)
        self.assertEqual(result, self.user)


    async def test_update_password(self):
        new_pasword = "1234567890"
        result = await update_password(password = "1234567890", current_user = self.user, db = self.session)
        self.assertEqual(result["user"].password, new_pasword)
        self.assertEqual(result["detail"], "Your password was update!")


if __name__ == '__main__':
    unittest.main()
