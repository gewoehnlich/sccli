import enum


class SoundcloudApiEndpointEnum(enum.Enum):
    AUTHORIZATION = "https://secure.soundcloud.com/authorize"
    TOKEN = "https://secure.soundcloud.com/oauth/token"

    API = "https://api.soundcloud.com"
