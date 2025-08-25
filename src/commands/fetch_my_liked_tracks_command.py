from src.actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction
from src.utils.run_action import run_action

def fetch_my_liked_tracks_command(args: list[str]) -> None:
    result: bool = run_action(
        FetchMyLikedTracksAction()
    )

    # to-do: handle true / false
