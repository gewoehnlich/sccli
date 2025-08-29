from sqlite3 import Cursor
from core.table import Table
from core.query_builder import QueryBuilder

class UsersTable(Table):
    def __init__(
        self,
        cursor: Cursor,
        query_builder: QueryBuilder
    ) -> None:
        super().__init__(
            cursor = cursor,
            query_builder = query_builder
        )

        self.name = "users"
        self.fields = [
            "avatar_url",
            "city",
            "country",
            "created_at",
            "description",
            "followers_count",
            "followings_count",
            "id",
            "kind",
            "last_modified",
            "permalink",
            "permalink_url",
            "plan",
            "track_count",
            "uri",
            "urn",
            "username",
        ]
