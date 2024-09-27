import unittest
from typing import Any

import requests

from tests.helpers import Generator


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._host = "127.0.0.1"
        self._port = 8000

    def tearDown(self) -> None:
        pass

    def test_create_valid_user(self) -> None:
        valid_user_data = {
            "name": f"{Generator.generate(7)} {Generator.generate(5)}",
            "email": f"{Generator.generate(7)}@{Generator.generate(5)}",
        }
        valid_post_response = requests.post(f"http://{self._host}:{self._port}/api/users", json=valid_user_data)
        invalid_post_response = requests.post(f"http://{self._host}:{self._port}/api/users", json=valid_user_data)
        self.assertEqual(valid_post_response.status_code, 201)
        self.assertEqual(invalid_post_response.status_code, 409)
        created_user = valid_post_response.json()
        self.assertEqual(valid_user_data["name"], created_user["name"])
        self.assertEqual(valid_user_data["email"], created_user["email"])
        self.assertEqual(valid_post_response.headers["Location"], f"/api/users/{created_user['id']}")
        requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")

    def test_create_invalid_user(self) -> None:
        invalid_user_data_400 = [
            {"name": f"{Generator.generate(5)} {Generator.generate(3)}"},
            {"email": f"{Generator.generate(5)}@{Generator.generate(3)}"},
            {},
            {"name": 5, "email": f"{Generator.generate(5)}@{Generator.generate(3)}"},
            {"name": f"{Generator.generate(6)}", "email": None},
            {"name": 999, "email": None},
        ]
        invalid_user_data_422 = [
            {"name": Generator.generate(1), "email": "aaa@bbb.ccc"},
            {"name": Generator.generate(7), "email": Generator.generate(10)},
            {"name": Generator.generate(1), "email": Generator.generate(10)},
            {"name": Generator.generate(7), "email": "@"},
        ]
        responses_400 = [
            requests.post(f"http://{self._host}:{self._port}/api/users", json=data)
            for data in invalid_user_data_400
        ]
        responses_422 = [
            requests.post(f"http://{self._host}:{self._port}/api/users", json=data)
            for data in invalid_user_data_422
        ]
        [self.assertEqual(response.status_code, 400) for response in responses_400]
        [self.assertEqual(response.status_code, 422) for response in responses_422]

    def test_get_user(self) -> None:
        invalid_get_response = requests.get(f"http://{self._host}:{self._port}/api/users/{1}")
        valid_user_data, created_user = self._create_valid_user()
        self.assertEqual(invalid_get_response.status_code, 404)
        valid_get_response = requests.get(f"http://{self._host}:{self._port}/api/users/{created_user["id"]}")
        gotten_user = valid_get_response.json()
        self.assertEqual(valid_get_response.status_code, 200)
        self.assertEqual(valid_user_data["email"], gotten_user["email"])
        self.assertEqual(valid_user_data["name"], gotten_user["name"])
        requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")

    def test_delete_user(self) -> None:
        valid_user_data, created_user = self._create_valid_user()
        delete_response_1 = requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")
        delete_response_2 = requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")
        self.assertEqual(delete_response_1.status_code, 204)
        self.assertEqual(delete_response_2.status_code, 404)

    def _create_valid_user(self) -> tuple[dict[str, Any], dict[str, Any]]:
        valid_user_data = {
            "name": f"{Generator.generate(7)} {Generator.generate(5)}",
            "email": f"{Generator.generate(7)}@{Generator.generate(5)}",
        }
        response = requests.post(f"http://{self._host}:{self._port}/api/users", json=valid_user_data)
        self.assertEqual(response.status_code, 201)
        created_user = response.json()
        self.assertEqual(valid_user_data["name"], created_user["name"])
        self.assertEqual(valid_user_data["email"], created_user["email"])
        return valid_user_data, created_user
