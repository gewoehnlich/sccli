import shlex
from typing import Tuple, List
from src.commands import get_track_streaming_url_command
from src.commands.followings_command import followings_command
from src.commands.followings_tracks_command import followings_tracks_command
from src.commands.get_track_command import get_track_command
from src.commands.get_track_streaming_url_command import get_track_streaming_url_command
from src.commands.help_command import help_command
from src.commands.exit_command import exit_command
from src.commands.my_tracks_command import my_tracks_command
from src.commands.unknown_command import unknown_command
from src.commands.user_command import user_command
from src.commands.users_liked_tracks_command import users_liked_tracks_command

def process_command(command_line: str) -> None:
    """Parses and executes a single command."""
    if not command_line:
        return

    command, args = parse_input(command_line)

    match command:
        case "help":
            help_command()
        case "me" | "user":
            user_command()
        case "tracks":
            users_liked_tracks_command(args)
        case "followings":
            followings_command(args)
        case "followings tracks":
            followings_tracks_command(args)
        case "my_tracks":
            my_tracks_command(args)
        case "track":
            get_track_command(args)
        case "track_streaming_url":
            get_track_streaming_url_command(args)
        case "exit" | "quit":
            exit_command()
        case _:
            unknown_command()

def parse_input(command_line: str) -> Tuple[str, List[str]]:
    parts: List[str] = shlex.split(command_line)
    if not parts:
        raise Exception("finish later. NO PARTS")

    command: str = parts[0].lower()
    args: List[str] = parts[1:]

    return command, args
