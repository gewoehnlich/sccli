from dependency_injector import containers, providers

from api_requests.authentication_request          import AuthenticationRequest
from api_requests.fetch_my_liked_tracks_request   import FetchMyLikedTracksRequest
from api_requests.followings_request              import FollowingsRequest
from api_requests.followings_tracks_request       import FollowingsTracksRequest
from api_requests.get_track_request               import GetTrackRequest
from api_requests.get_track_streaming_url_request import GetTrackStreamingUrlRequest
from api_requests.me_tracks_request               import MeTracksRequest
from api_requests.refresh_token_request           import RefreshTokenRequest
from api_requests.user_info_request               import UserInfoRequest


class RequestsContainer(
    containers.DeclarativeContainer
):
    authentication = providers.Factory(
        AuthenticationRequest,
    )
    fetch_my_liked_tracks = providers.Factory(
        FetchMyLikedTracksRequest,
    )
    followings = providers.Factory(
        FollowingsRequest
    )
    followings_tracks = providers.Factory(
        FollowingsTracksRequest
    )
    get_track = providers.Factory(
        GetTrackRequest
    )
    get_track_streaming_url = providers.Factory(
        GetTrackStreamingUrlRequest
    )
    me_tracks = providers.Factory(
        MeTracksRequest
    )
    refresh_token = providers.Factory(
        RefreshTokenRequest,
    )
    user_info = providers.Factory(
        UserInfoRequest
    )
