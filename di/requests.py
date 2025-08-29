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


class Requests:
    def __init__(self) -> None:
        self.authentication_request = authentication_request,
        self.fetch_my_liked_tracks_request = fetch_my_liked_tracks_request,
        self.followings_request = followings_request,
        self.followings_tracks_request = followings_tracks_request,
        self.get_track_request = get_track_request,
        self.me_tracks_request = me_tracks_request,
        self.next_href_request = next_href_request,
        self.refresh_token_request = refresh_token_request,
        self.user_info_request = user_info_request,
