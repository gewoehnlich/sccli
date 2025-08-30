from typing import Callable
from commands.exit_command import exit_command
from commands.fetch_my_liked_tracks_command import fetch_my_liked_tracks_command
from commands.followings_command import followings_command
from commands.followings_tracks_command import followings_tracks_command
from commands.get_track_command import get_track_command
from commands.get_track_streaming_url_command import get_track_streaming_url_command
from commands.help_command import help_command
# from commands.load_soundcloud_tracks import load_soundcloud_tracks
from commands.my_tracks_command import my_tracks_command
# from commands.sync_tracks import sync_tracks
from commands.unknown_command import unknown_command
from commands.user_command import user_command
from commands.welcome_command import welcome_command
from core.di_container import DiContainer
from dependency_injector import containers, providers

class CommandsContainer(containers.DeclarativeContainer):
    exit = providers.Callable(exit_command)
    fetch_my_liked_tracks = providers.Callable(fetch_my_liked_tracks_command)
    followings = providers.Callable(followings_command)
    followings_tracks = providers.Callable(followings_tracks_command)
    get_track = providers.Callable(get_track_command)
    get_track_streaming_url = providers.Callable(get_track_streaming_url_command)
    help = providers.Callable(help_command)
    # load_soundcloud_tracks = providers.Callable(load_soundcloud_tracks)
    my_tracks = providers.Callable(my_tracks_command)
    # sync_tracks = providers.Callable(sync_tracks)
    unknown = providers.Callable(unknown_command)
    user = providers.Callable(user_command)
    welcome = providers.Callable(welcome_command)

class Test:
    welcome: Callable = welcome_command
