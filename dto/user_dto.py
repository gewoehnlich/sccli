from datetime import datetime
from typing import Any, Self

from core.dto import Dto
from enums.kinds import KindsEnum


class UserDto(Dto):
    KIND: KindsEnum = KindsEnum.USER

    avatar_url:             str
    city:                   str      | None
    country:                str      | None
    created_at:             datetime
    description:            str      | None
    followers_count:        int
    followings_count:       int
    id:                     int
    last_modified:          datetime
    permalink:              str
    permalink_url:          str
    playlists_count:        int
    public_favorites_count: int
    reposts_count:          int
    track_count:            int
    uri:                    str
    urn:                    str
    username:               str

    def from_dict(
        self,
        data: dict[str, Any],
    ) -> Self:
        self.validate_kind(
            actual_kind   = data["kind"],
            expected_kind = self.KIND,
        )

        self.avatar_url             = data["avatar_url"]
        self.city                   = data["city"]
        self.country                = data["country"]
        self.created_at             = data["created_at"]
        self.description            = data["description"]
        self.followers_count        = data["followers_count"]
        self.followings_count       = data["followings_count"]
        self.id                     = data["id"]
        self.last_modified          = data["last_modified"]
        self.permalink              = data["permalink"]
        self.permalink_url          = data["permalink_url"]
        self.playlists_count        = data["playlists_count"]
        self.public_favorites_count = data["public_favorites_count"]
        self.reposts_count          = data["reposts_count"]
        self.track_count            = data["track_count"]
        self.uri                    = data["uri"]
        self.urn                    = data["urn"]
        self.username               = data["username"]
