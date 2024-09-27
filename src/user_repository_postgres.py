import os
from typing import Any

import psycopg as pg

from custom_exceptions import ConflictException, NotFoundException
from postgres_row_factories import DictRowFactory


class UserRepositoryPostgreSQL:
    def __init__(self) -> None:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = int(os.getenv("POSTGRES_PORT"))
        database = os.getenv("POSTGRES_DB")
        self._url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def create_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        by_email_query = """
            SELECT * FROM public.users WHERE email = %s;
        """
        query = """
            INSERT INTO public.users (name, email) VALUES (%s, %s) RETURNING *;
        """
        by_email_parameters = (user_data["email"],)
        parameters = (user_data["name"], user_data["email"])
        with pg.connect(self._url, row_factory=DictRowFactory) as connection:
            cursor = connection.execute(by_email_query.encode(), by_email_parameters)
            conflicting_user = cursor.fetchone()
            if conflicting_user is not None:
                raise ConflictException("An user with that email already exists")
            cursor = connection.execute(query.encode(), parameters)
            created_user = cursor.fetchone()
        return created_user

    def get_user(self, user_id: int) -> dict[str, Any]:
        with pg.connect(self._url, row_factory=DictRowFactory) as connection:
            query = """
                    SELECT * FROM public.users WHERE id = %s;
                """
            parameters = user_id,
            cursor = connection.execute(query.encode(), parameters)
            fetched_user = cursor.fetchone()
            if fetched_user is None:
                raise NotFoundException("User not found")
            return fetched_user

    def delete_user(self, user_id: int) -> None:
        with pg.connect(self._url, row_factory=DictRowFactory) as connection:
            query = """
                    DELETE FROM public.users WHERE id = %s RETURNING id;
                """
            parameters = (user_id,)
            cursor = connection.execute(query.encode(), parameters)
            deleted_user = cursor.fetchone()
            if deleted_user is None:
                raise NotFoundException("User not found")
