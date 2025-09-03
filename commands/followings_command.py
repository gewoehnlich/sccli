from requests_.followings_request import FollowingsRequest
from pprint import pprint


def followings_command(
    action: Action,
    args: list[str],
) -> None:
    result: bool = action()
    pprint(result.json())
