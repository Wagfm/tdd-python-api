import unittest

from custom_exceptions import ConflictException
from tests.helpers import Generator
from user_repository_postgres import UserRepositoryPostgreSQL


class TestPostgresRepository(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_user(self) -> None:
        valid_user_data = {
            "name": f"{Generator.generate(6)} {Generator.generate(4)}",
            "email": f"{Generator.generate(10)}@{Generator.generate(5)}",
        }
        repository = UserRepositoryPostgreSQL()
        created_user = repository.create_user(valid_user_data)
        fetched_user = repository.get_user(created_user["id"])
        self.assertEqual(fetched_user["name"], valid_user_data["name"])
        self.assertEqual(fetched_user["email"], valid_user_data["email"])
        self.assertRaises(ConflictException, repository.create_user, valid_user_data)
        repository.delete_user(created_user["id"])
