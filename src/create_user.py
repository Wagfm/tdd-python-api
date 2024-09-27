from typing import Any

from custom_exceptions import MissingFieldException, WrongDataTypeException
from user_repository_postgres import UserRepositoryPostgreSQL


class CreateUser:
    def __init__(self) -> None:
        pass

    def execute(self, user_data: dict[str, Any]) -> dict[str, Any]:
        user_repository = UserRepositoryPostgreSQL()
        if "email" not in user_data:
            raise MissingFieldException("Missing 'email' key in user data")
        if "name" not in user_data:
            raise MissingFieldException("Missing 'name' key in user data")
        if not isinstance(user_data["email"], str):
            raise WrongDataTypeException("Email must be a string")
        if not isinstance(user_data["name"], str):
            raise WrongDataTypeException("Name must be a string")
        if "@" not in user_data["email"] or len(user_data["email"]) < 3:
            raise ValueError("Invalid email address")
        if len(user_data["name"]) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(user_data["email"]) > 50:
            raise ValueError("Email address too long")
        if len(user_data["name"]) > 50:
            raise ValueError("User name too long")
        return user_repository.create_user(user_data)
