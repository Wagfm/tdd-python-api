from collections.abc import Sequence
from typing import Any

from psycopg import Cursor


class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        if cursor.description is None:
            self.fields = []
            return
        self.fields = [c.name for c in cursor.description]

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self.fields, values))
