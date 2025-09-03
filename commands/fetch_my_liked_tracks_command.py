from actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction
from core.action import Action


def fetch_my_liked_tracks_command(
    action: Action,
    args: list[str],
) -> None:
    result: bool = action()

    # to-do: handle true / false
