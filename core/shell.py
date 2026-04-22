import shlex
from typing import Tuple
from di.commands_container import CommandsContainer


class Shell:
    commands: CommandsContainer

    def __init__(
        self,
        commands: CommandsContainer,
    ) -> None:
        self.commands = commands

    def run(
        self,
    ) -> None:
        """Starts the interactive shell session."""
        self.commands.welcome.run()

        while True:
            try:
                command_line: str = input("sccli> ")
                self.__process_command(command_line=command_line)
            except KeyboardInterrupt:
                self.commands.exit.run()
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def __process_command(
        self,
        command_line: str,
    ) -> None:
        """Parses and executes the command."""
        if not command_line:
            return

        command, args = self.__parse_input(command_line)

        match command:
            case "help":
                self.commands.help.run()
            case "liked:tracks" | "lt":
                self.commands.liked_tracks.run()
            case "track:play" | "tp":
                self.commands.play.run()
            case "exit" | "quit" | "q":
                self.commands.exit.run()

            case _:
                self.commands.unknown.run()

    def __parse_input(
        self,
        command_line: str
    ) -> Tuple[str, list[str]]:
        parts: list[str] = shlex.split(command_line)

        command: str = parts[0].lower()
        args: list[str] = parts[1:]

        return command, args
