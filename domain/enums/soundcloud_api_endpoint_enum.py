from enum import Enum


class SoundcloudApiEndpointEnum(Enum):
    AUTHORIZATION = "https://secure.soundcloud.com/authorize"
    TOKEN = "https://secure.soundcloud.com/oauth/token"
    REFRESH_TOKEN = "https://secure.soundcloud.com/oauth/token"
    API = "https://api.soundcloud.com"
