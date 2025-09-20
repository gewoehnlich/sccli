from typing import Any, Self

from core.dto import Dto
from enums.kinds import KindsEnum


class UserDto(Dto):
    KIND = KindsEnum.USER

    avatar_url:             str
    city:                   str | None
    country:                str | None
    created_at:             str
    description:            str | None
    followers_count:        int
    followings_count:       int
    id:                     int
    last_modified:          str
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

        self.avatar_url: str = data["avatar_url"]
        self.city: str = data["city"]
        self.country: str = data["country"]
        self.created_at: str = data["created_at"]
        self.description: str | None = data["description"]
        self.followers_count: int = data["followers_count"]
        self.followings_count: int = data["followings_count"]
        self.id: int = data["id"]
        self.last_modified: str = data["last_modified"]
        self.permalink: str = data["permalink"]
        self.permalink_url: str = data["permalink_url"]
        self.playlists_count: int = data["playlists_count"]
        self.public_favorites_count: int = data["public_favorites_count"]
        self.reposts_count: int = data["reposts_count"]
        self.track_count: int = data["track_count"]
        self.uri: str = data["uri"]
        self.urn: str = data["urn"]
        self.username: str = data["username"]
