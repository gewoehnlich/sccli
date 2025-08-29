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


class Commands:
    def __init__(self) -> None:
        self.exit_command = exit_command,
        self.fetch_my_liked_tracks_command = fetch_my_liked_tracks_command,
        self.followings_command = followings_command,
        self.followings_tracks_command = followings_tracks_command,
        self.get_track_command = get_track_command,
        self.get_track_streaming_url_command = get_track_streaming_url_command,
        self.help_command = help_command,
        self.load_soundcloud_tracks_command = load_soundcloud_tracks
        self.my_tracks_command = my_tracks_command,
        self.sync_tracks_command = sync_tracks,
        self.unknown_command = unknown_command,
        self.user_command = user_command,
        self.welcome_command = welcome_command,
