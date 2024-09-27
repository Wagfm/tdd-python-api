import os
from typing import Any, Optional

import psycopg as pg
from psycopg import Connection

from custom_exceptions import NotFoundException
from postgres_row_factories import DictRowFactory


class GetUser:
    def __init__(self) -> None:
        pass

    def execute(self, user_id: int) -> dict[str, Any]:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = int(os.getenv("POSTGRES_PORT"))
        database = os.getenv("POSTGRES_DB")
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        connection: Optional[Connection] = None
        try:
            query = """
                SELECT * FROM public.users WHERE id = %s;
            """
            parameters = user_id,
            connection = pg.connect(url, row_factory=DictRowFactory)
            cursor = connection.execute(query.encode(), parameters)
            fetched_user = cursor.fetchone()
        except Exception:
            raise
        finally:
            if connection is not None:
                connection.close()
        if fetched_user is None:
            raise NotFoundException("User not found")
        return fetched_user
