from user_repository_postgres import UserRepositoryPostgreSQL


class DeleteUser:
    def __init__(self) -> None:
        pass

    def execute(self, user_id: int) -> None:
        user_repository = UserRepositoryPostgreSQL()
        user_repository.delete_user(user_id)
