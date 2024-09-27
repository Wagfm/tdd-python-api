from typing import Any

from user_repository_postgres import UserRepositoryPostgreSQL


class GetUser:
    def __init__(self) -> None:
        pass

    def execute(self, user_id: int) -> dict[str, Any]:
        user_repository = UserRepositoryPostgreSQL()
        return user_repository.get_user(user_id)
