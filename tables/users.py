from core.table import Table

class UsersTable(Table):
    def __init__(self):
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
