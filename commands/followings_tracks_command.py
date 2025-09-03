from requests_.followings_tracks_request import FollowingsTracksRequest
from pprint import pprint

def followings_tracks_command(
    action: Action,
    args: list[str],
) -> None:
    result: bool = action()
    pprint(result.json())
