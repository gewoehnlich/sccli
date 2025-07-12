import shlex
from typing import Tuple, List, Optional
from src.commands.help import help_command
from src.commands.exit import exit_command
from src.commands.unknown import unknown_command

def process_command(command_line: str) -> None:
    """Parses and executes a single command."""
    if not command_line:
        return

    command, args = parse_input(command_line)

    match command:
        case "help":
            help_command()
        case "exit" | "quit":
            exit_command()
        case _:
            unknown_command()

def parse_input(command_line: str) -> Optional[Tuple[str, List[str]]]:
    parts = shlex.split(command_line)
    if not parts:
        raise Exception()

    command = parts[0].lower()
    args = parts[1:]

    return command, args
