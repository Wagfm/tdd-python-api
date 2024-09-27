import random
import string
import unittest

import requests


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._host = "127.0.0.1"
        self._port = 8000

    def tearDown(self) -> None:
        pass

    def test_create_valid_user(self) -> None:
        valid_user_data = {
            "name": f"{self._generator(7)} {self._generator(5)}",
            "email": self._generator(25)
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
        invalid_user_data_1 = {
            "name": self._generator(1),
            "email": self._generator(25)
        }
        invalid_user_data_2 = {
            "name": self._generator(10),
            "email": self._generator(2)
        }
        invalid_user_data_3 = {
            "email": self._generator(10)
        }
        invalid_user_data_4 = {
            "name": self._generator(10)
        }
        response_1 = requests.post(f"http://{self._host}:{self._port}/api/users", json=invalid_user_data_1)
        response_2 = requests.post(f"http://{self._host}:{self._port}/api/users", json=invalid_user_data_2)
        response_3 = requests.post(f"http://{self._host}:{self._port}/api/users", json=invalid_user_data_3)
        response_4 = requests.post(f"http://{self._host}:{self._port}/api/users", json=invalid_user_data_4)
        self.assertEqual(response_1.status_code, 422)
        self.assertEqual(response_2.status_code, 422)
        self.assertEqual(response_3.status_code, 422)
        self.assertEqual(response_4.status_code, 422)

    def test_get_user(self) -> None:
        invalid_get_response = requests.get(f"http://{self._host}:{self._port}/api/users/{1}")
        self.assertEqual(invalid_get_response.status_code, 404)
        valid_user_data = {
            "name": f"{self._generator(10)} {self._generator(5)}",
            "email": self._generator(25)
        }
        post_response = requests.post(f"http://{self._host}:{self._port}/api/users", json=valid_user_data)
        self.assertEqual(post_response.status_code, 201)
        created_user = post_response.json()
        self.assertEqual(valid_user_data["name"], created_user["name"])
        self.assertEqual(valid_user_data["email"], created_user["email"])
        valid_get_response = requests.get(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")
        gotten_user = valid_get_response.json()
        self.assertEqual(valid_get_response.status_code, 200)
        self.assertEqual(valid_user_data["email"], gotten_user["email"])
        self.assertEqual(valid_user_data["name"], gotten_user["name"])
        requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")

    def test_delete_user(self) -> None:
        valid_user_data = {
            "name": f"{self._generator(9)} {self._generator(5)}",
            "email": self._generator(25)
        }
        post_response = requests.post(f"http://{self._host}:{self._port}/api/users", json=valid_user_data)
        self.assertEqual(post_response.status_code, 201)
        created_user = post_response.json()
        self.assertEqual(valid_user_data["name"], created_user["name"])
        self.assertEqual(valid_user_data["email"], created_user["email"])
        delete_response_1 = requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")
        delete_response_2 = requests.delete(f"http://{self._host}:{self._port}/api/users/{created_user['id']}")
        self.assertEqual(delete_response_1.status_code, 204)
        self.assertEqual(delete_response_2.status_code, 404)

    def _generator(self, string_length: int) -> str:
        return str.join("", random.choices(string.ascii_letters, k=string_length)).lower()
