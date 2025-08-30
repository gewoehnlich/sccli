from commands import (
    exit_command,
    fetch_my_liked_tracks_command,
    followings_command,
    followings_tracks_command,
    get_track_command,
    get_track_streaming_url_command,
    help_command,
    load_soundcloud_tracks,
    my_tracks_command,
    sync_tracks,
    unknown_command,
    user_command,
    welcome_command
)
from core.di_container import DiContainer


class CommandsContainer(DiContainer):
    exit = exit_command
    fetch_my_liked_tracks = fetch_my_liked_tracks_command
    followings = followings_command
    followings_tracks = followings_tracks_command
    get_track = get_track_command
    get_track_streaming_url = get_track_streaming_url_command
    help = help_command
    load_soundcloud_tracks = load_soundcloud_tracks
    my_tracks = my_tracks_command
    sync_tracks = sync_tracks
    unknown = unknown_command
    user = user_command
    welcome = welcome_command
