import os
from typing import Optional

import psycopg as pg
from psycopg import Connection

from custom_exceptions import NotFoundException
from postgres_row_factories import DictRowFactory


class DeleteUser:
    def __init__(self) -> None:
        pass

    def execute(self, user_id: int) -> None:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = int(os.getenv("POSTGRES_PORT"))
        database = os.getenv("POSTGRES_DB")
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        connection: Optional[Connection] = None
        try:
            query = """
                DELETE FROM public.users WHERE id = %s RETURNING id;
            """
            parameters = (user_id,)
            connection = pg.connect(url, row_factory=DictRowFactory)
            cursor = connection.execute(query.encode(), parameters)
            deleted_user = cursor.fetchone()
        except Exception:
            if connection is not None:
                connection.rollback()
            raise
        finally:
            if connection is not None:
                connection.commit()
                connection.close()
        if deleted_user is None:
            raise NotFoundException("User not found")
