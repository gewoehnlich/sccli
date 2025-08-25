import shlex
from typing import Tuple, List
from src.commands.fetch_my_liked_tracks_command import fetch_my_liked_tracks_command
from src.commands.followings_command import followings_command
from src.commands.followings_tracks_command import followings_tracks_command
from src.commands.get_track_command import get_track_command
from src.commands.get_track_streaming_url_command import get_track_streaming_url_command
from src.commands.help_command import help_command
from src.commands.exit_command import exit_command
from src.commands.my_tracks_command import my_tracks_command
from src.commands.unknown_command import unknown_command
from src.commands.user_command import user_command

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
        case "liked:tracks" | "lt":
            fetch_my_liked_tracks_command(args)
        case "me:followings":
            followings_command(args)
        case "me:followings:tracks":
            followings_tracks_command(args)
        case "me:tracks":
            my_tracks_command(args)
        case "track":
            get_track_command(args)
        case "track_streaming_url":
            get_track_streaming_url_command(args)
        case "exit" | "quit" | "q":
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
