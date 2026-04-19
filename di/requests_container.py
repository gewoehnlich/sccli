from api_requests.authentication_request          import AuthenticationRequest
from api_requests.fetch_my_liked_tracks_request   import FetchMyLikedTracksRequest
from api_requests.followings_request              import FollowingsRequest
from api_requests.followings_tracks_request       import FollowingsTracksRequest
from api_requests.get_track_request               import GetTrackRequest
from api_requests.get_track_streaming_url_request import GetTrackStreamingUrlRequest
from api_requests.me_tracks_request               import MeTracksRequest
from api_requests.refresh_token_request           import RefreshTokenRequest
from api_requests.user_info_request               import UserInfoRequest
from core.auth import Auth
from di.dto_container import DtoContainer


class RequestsContainer(

):
    def __init__(
        self,
        auth: Auth,
        dto: DtoContainer
    ):
        print(123)
        #
        # self.fetch_my_liked_tracks = FetchMyLikedTracksRequest(
        #     auth = auth,
        #     # dto = dto.fetch_my_liked_tracks,
        # )
    # followings = FollowingsRequest
    # followings_tracks = FollowingsTracksRequest
    # get_track = GetTrackRequest
    # get_track_streaming_url = GetTrackStreamingUrlRequest
    # me_tracks = MeTracksRequest
    # user_info = UserInfoRequest
