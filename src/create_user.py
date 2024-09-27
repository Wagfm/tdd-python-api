import os
from typing import Any, Optional

import psycopg as pg
from psycopg import Connection

from custom_exceptions import ConflictException
from postgres_row_factories import DictRowFactory


class CreateUser:
    def __init__(self) -> None:
        pass

    def execute(self, user_data: dict[str, Any]) -> dict[str, Any]:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = int(os.getenv("POSTGRES_PORT"))
        database = os.getenv("POSTGRES_DB")
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        connection: Optional[Connection] = None
        try:
            by_email_query = """
                SELECT * FROM public.users WHERE email = %s;
            """
            query = """
                INSERT INTO public.users (name, email) VALUES (%s, %s) RETURNING *;
            """
            by_email_parameters = (user_data["email"],)
            parameters = (user_data["name"], user_data["email"])
            connection = pg.connect(url, row_factory=DictRowFactory)
            cursor = connection.execute(by_email_query.encode(), by_email_parameters)
            conflicting_user = cursor.fetchone()
            if conflicting_user is not None:
                raise ConflictException("An user with that email already exists")
            cursor = connection.execute(query.encode(), parameters)
            connection.commit()
            created_user = cursor.fetchone()
        except Exception:
            if connection is not None:
                connection.rollback()
            raise
        finally:
            if connection is not None:
                connection.close()
        return created_user
