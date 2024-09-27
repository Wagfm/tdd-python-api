import unittest

from create_user import CreateUser
from custom_exceptions import ConflictException, WrongDataTypeException, MissingFieldException, NotFoundException
from delete_user import DeleteUser
from get_user import GetUser
from tests.helpers import Generator


class TestUseCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_valid_user(self) -> None:
        valid_user_data = {
            "name": f"{Generator.generate(5)} {Generator.generate(3)}",
            "email": f"{Generator.generate(6)}@{Generator.generate(10)}",
        }
        create_user = CreateUser()
        delete_user = DeleteUser()
        created_user = create_user.execute(valid_user_data)
        self.assertEqual(valid_user_data["name"], created_user["name"])
        self.assertEqual(valid_user_data["email"], created_user["email"])
        self.assertRaises(ConflictException, create_user.execute, valid_user_data)
        delete_user.execute(created_user["id"])

    def test_create_invalid_user(self) -> None:
        invalid_user_data_1 = {"name": f"{Generator.generate(5)} {Generator.generate(3)}"}
        invalid_user_data_2 = {"email": f"{Generator.generate(5)}@{Generator.generate(3)}"}
        invalid_user_data_3 = {}
        invalid_user_data_4 = {"name": 5, "email": f"{Generator.generate(5)}@{Generator.generate(3)}"}
        invalid_user_data_5 = {"name": f"{Generator.generate(6)}", "email": None}
        invalid_user_data_6 = {"name": 999, "email": None}
        invalid_user_data_7 = {"name": Generator.generate(1), "email": "aaa@bbb.ccc"}
        invalid_user_data_8 = {"name": Generator.generate(7), "email": Generator.generate(10)}
        invalid_user_data_9 = {"name": Generator.generate(1), "email": Generator.generate(10)}
        invalid_user_data_10 = {"name": Generator.generate(7), "email": "@"}
        create_user = CreateUser()
        self.assertRaises(MissingFieldException, create_user.execute, invalid_user_data_1)
        self.assertRaises(MissingFieldException, create_user.execute, invalid_user_data_2)
        self.assertRaises(MissingFieldException, create_user.execute, invalid_user_data_3)
        self.assertRaises(WrongDataTypeException, create_user.execute, invalid_user_data_4)
        self.assertRaises(WrongDataTypeException, create_user.execute, invalid_user_data_5)
        self.assertRaises(WrongDataTypeException, create_user.execute, invalid_user_data_6)
        self.assertRaises(ValueError, create_user.execute, invalid_user_data_7)
        self.assertRaises(ValueError, create_user.execute, invalid_user_data_8)
        self.assertRaises(ValueError, create_user.execute, invalid_user_data_9)
        self.assertRaises(ValueError, create_user.execute, invalid_user_data_10)

    def test_get_user(self) -> None:
        valid_user_data = {
            "name": f"{Generator.generate(5)} {Generator.generate(3)}",
            "email": f"{Generator.generate(6)}@{Generator.generate(10)}",
        }
        get_user = GetUser()
        create_user = CreateUser()
        delete_user = DeleteUser()
        created_user = create_user.execute(valid_user_data)
        self.assertRaises(NotFoundException, get_user.execute, -1)
        self.assertRaises(NotFoundException, get_user.execute, 0)
        self.assertRaises(NotFoundException, get_user.execute, 1)
        fetched_user = get_user.execute(created_user["id"])
        fetched_user.pop("id")
        self.assertDictEqual(valid_user_data, fetched_user)
        delete_user.execute(created_user["id"])

    def test_delete_user(self) -> None:
        valid_user_data = {
            "name": f"{Generator.generate(5)} {Generator.generate(3)}",
            "email": f"{Generator.generate(6)}@{Generator.generate(10)}",
        }
        create_user = CreateUser()
        delete_user = DeleteUser()
        self.assertRaises(NotFoundException, delete_user.execute, -1)
        self.assertRaises(NotFoundException, delete_user.execute, 0)
        self.assertRaises(NotFoundException, delete_user.execute, 1)
        created_user = create_user.execute(valid_user_data)
        user_id = created_user.pop("id")
        delete_user.execute(user_id)
        self.assertRaises(NotFoundException, delete_user.execute, user_id)
