from typing import Any, Self

from core.dto import Dto
from dto.user_dto import UserDto
from enums.kinds import KindsEnum


class TrackDto(Dto):
    KIND = KindsEnum.TRACK

    access:              str
    artwork_url:         str
    comments_count:      int
    created_at:          str
    description:         str | None
    duration:            int
    favoritings_count:   int
    id:                  int
    metadata_artist:     str | None
    permalink_url:       str
    playback_count:      int
    reposts_count:       int
    stream_url:          str
    title:               str
    uri:                 str
    urn:                 str
    user:                UserDto
    user_favorite:       bool
    user_playback_count: int

    def from_dict(
        self,
        data: dict[str, Any],
    ) -> Self:
        self.validate_kind(
            actual_kind   = data["kind"],
            expected_kind = self.KIND,
        )

        self.access: str = data["access"]
        self.artwork_url: str = data["artwork_url"]
        self.comments_count: int = data["comments_count"]
        self.created_at: str = data["created_at"]
        self.description: str | None = data["description"]
        self.duration: int = data["duration"]
        self.favoritings_count: int = data["favoritings_count"]
        self.id: int = data["id"]
        self.metadata_artist: str | None = data["metadata_artist"]
        self.permalink_url: str = data["permalink_url"]
        self.playback_count: int = data["playback_count"]
        self.reposts_count: int = data["reposts_count"]
        self.stream_url: str = data["stream_url"]
        self.title: str = data["title"]
        self.uri: str = data["uri"]
        self.urn: str = data["urn"]
        self.user: UserDto = UserDto.from_dict(
            data = data["user"]
        )
        self.user_favorite: bool = data["user_favorite"]
        self.user_playback_count: int = data["user_playback_count"]

        return self
