from dependency_injector import containers, providers
from requests_.authentication_request import AuthenticationRequest
from requests_.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from requests_.followings_request import FollowingsRequest
from requests_.followings_tracks_request import FollowingsTracksRequest
from requests_.get_track_request import GetTrackRequest
from requests_.me_tracks_request import MeTracksRequest
from requests_.next_href_request import NextHrefRequest
from requests_.refresh_token_request import RefreshTokenRequest
from requests_.user_info_request import UserInfoRequest


class RequestsContainer(containers.DeclarativeContainer):
    authentication = providers.Callable(AuthenticationRequest)
    fetch_my_liked_tracks = providers.Callable(FetchMyLikedTracksRequest)
    followings = providers.Callable(FollowingsRequest)
    followings_tracks = providers.Callable(FollowingsTracksRequest)
    get_track = providers.Callable(GetTrackRequest)
    me_tracks = providers.Callable(MeTracksRequest)
    next_href = providers.Callable(NextHrefRequest)
    refresh_token = providers.Callable(RefreshTokenRequest)
    user_info = providers.Callable(UserInfoRequest)
