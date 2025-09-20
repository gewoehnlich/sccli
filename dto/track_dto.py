from core.dto import Dto
from dto.user_dto import UserDto


class TrackDto(Dto):
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
