from api_requests.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from api_requests.fetch_track_from_streaming_url_request import (
    FetchTrackFromStreamingUrlRequest,
)
from api_requests.fetch_track_streams_request import FetchTrackStreamsRequest


class RequestsContainer:
    fetch_my_liked_tracks = FetchMyLikedTracksRequest
    fetch_track_streams = FetchTrackStreamsRequest
    fetch_track_from_streaming_url = FetchTrackFromStreamingUrlRequest
