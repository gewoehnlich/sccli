from actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction
from utils.run_action import run_action

def fetch_my_liked_tracks_command(self, args: list[str]) -> None:
    result: bool = run_action(
        FetchMyLikedTracksAction()
    )

    # to-do: handle true / false
