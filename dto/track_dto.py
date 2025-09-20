from datetime import datetime
from typing import Any, Self

from core.dto import Dto
from dto.user_dto import UserDto
from enums.kinds import KindsEnum


class TrackDto(Dto):
    KIND: KindsEnum = KindsEnum.TRACK

    access:              str
    artwork_url:         str
    comments_count:      int
    created_at:          datetime
    description:         str      | None
    duration:            int
    favoritings_count:   int
    id:                  int
    metadata_artist:     str      | None
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

        self.access            = data["access"]
        self.artwork_url       = data["artwork_url"]
        self.comments_count    = data["comments_count"]
        self.created_at        = data["created_at"]
        self.description       = data["description"]
        self.duration          = data["duration"]
        self.favoritings_count = data["favoritings_count"]
        self.id                = data["id"]
        self.metadata_artist   = data["metadata_artist"]
        self.permalink_url     = data["permalink_url"]
        self.playback_count    = data["playback_count"]
        self.reposts_count     = data["reposts_count"]
        self.stream_url        = data["stream_url"]
        self.title             = data["title"]
        self.uri               = data["uri"]
        self.urn               = data["urn"]
        self.user = UserDto.from_dict(
            data = data["user"]
        )
        self.user_favorite       = data["user_favorite"]
        self.user_playback_count = data["user_playback_count"]

        return self
