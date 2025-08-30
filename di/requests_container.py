from core.di_container import DiContainer
from requests_ import (
    authentication_request, 
    fetch_my_liked_tracks_request, 
    followings_request, 
    followings_tracks_request, 
    get_track_request, 
    me_tracks_request, 
    next_href_request, 
    refresh_token_request, 
    user_info_request
)


class RequestsContainer(DiContainer):
    def __init__(self) -> None:
        self.authentication = authentication_request
        self.fetch_my_liked_tracks = fetch_my_liked_tracks_request
        self.followings = followings_request
        self.followings_tracks = followings_tracks_request
        self.get_track = get_track_request
        self.me_tracks = me_tracks_request
        self.next_href = next_href_request
        self.refresh_token = refresh_token_request
        self.user_info = user_info_request
