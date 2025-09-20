from dependency_injector import containers, providers

from requests_.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from requests_.followings_request import FollowingsRequest
from requests_.followings_tracks_request import FollowingsTracksRequest
from requests_.get_track_request import GetTrackRequest
from requests_.get_track_streaming_url_request import GetTrackStreamingUrlRequest
from requests_.me_tracks_request import MeTracksRequest
from requests_.user_info_request import UserInfoRequest


class RequestsContainer(containers.DeclarativeContainer):
    auth = providers.Dependency()
    dto  = providers.DependenciesContainer()

    fetch_my_liked_tracks   = providers.Factory(
        FetchMyLikedTracksRequest,
        auth = auth,
        dto  = dto,
    )
    followings              = providers.Factory(FollowingsRequest)
    followings_tracks       = providers.Factory(FollowingsTracksRequest)
    get_track               = providers.Factory(GetTrackRequest)
    get_track_streaming_url = providers.Factory(GetTrackStreamingUrlRequest)
    me_tracks               = providers.Factory(MeTracksRequest)
    user_info               = providers.Factory(UserInfoRequest)
