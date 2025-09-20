from core.dto import Dto


class UserDto(Dto):
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
