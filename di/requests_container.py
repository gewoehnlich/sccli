from dependency_injector import containers, providers

from requests_.authentication_request import AuthenticationRequest
from requests_.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from requests_.followings_request import FollowingsRequest
from requests_.followings_tracks_request import FollowingsTracksRequest
from requests_.get_track_request import GetTrackRequest
from requests_.get_track_streaming_url_request import GetTrackStreamingUrlRequest
from requests_.me_tracks_request import MeTracksRequest
from requests_.refresh_token_request import RefreshTokenRequest
from requests_.user_info_request import UserInfoRequest


class RequestsContainer(containers.DeclarativeContainer):
    authentication          = providers.Object(AuthenticationRequest)
    fetch_my_liked_tracks   = providers.Object(FetchMyLikedTracksRequest)
    followings              = providers.Object(FollowingsRequest)
    followings_tracks       = providers.Object(FollowingsTracksRequest)
    get_track               = providers.Object(GetTrackRequest)
    get_track_streaming_url = providers.Object(GetTrackStreamingUrlRequest)
    me_tracks               = providers.Object(MeTracksRequest)
    refresh_token           = providers.Object(RefreshTokenRequest)
    user_info               = providers.Object(UserInfoRequest)
