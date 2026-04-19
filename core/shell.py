import shlex
from typing import Tuple, List
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
                self.process_command(command_line = command_line)

            except KeyboardInterrupt:
                self.commands.exit.run()
                break

            except Exception as e:
                print(f"An unexpected error occurred: {e}")


    def process_command(
        self,
        command_line: str = "",
    ) -> None:
        """Parses and executes the command."""
        if not command_line:
            return

        command, args = self.parse_input(command_line)

        match command:
            case "help":
                self.commands.help.run()
            case "me" | "user":
                self.commands.user().run()
            case "liked:tracks" | "lt":
                self.commands.my_liked_tracks(args).run()
            case "me:followings":
                self.commands.followings(args).run()
            case "me:followings:tracks":
                self.commands.followings_tracks(args).run()
            case "me:tracks":
                self.commands.my_tracks(args).run()
            case "track":
                self.commands.track(args).run()
            case "track_streaming_url":
                self.commands.track_streaming_url(args).run()
            case "exit" | "quit" | "q":
                self.commands.exit.run()
            case _:
                self.commands.unknown_command.run()


    def parse_input(
        self,
        command_line: str
    ) -> Tuple[str, List[str]]:
        parts: List[str] = shlex.split(command_line)
        if not parts:
            raise Exception("finish later. NO PARTS")

        command: str = parts[0].lower()
        args: List[str] = parts[1:]

        return command, args
