import shlex
from typing import Tuple, List
from dependency_injector.wiring import Provide, inject
from core.di_container import DiContainer
from di.commands_container import CommandsContainer


class Shell:
    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @inject
    def run(
        self,
        commands: CommandsContainer = Provide[DiContainer.commands]
    ) -> None:
        """Starts the interactive shell session."""
        commands.welcome().run()

        while True:
            try:
                command_line: str = input("sccli> ")
                self.process_command(command_line = command_line)

            except KeyboardInterrupt:
                commands.exit().run()
                break

            except Exception as e:
                print(f"An unexpected error occurred: {e}")


    @inject
    def process_command(
        self,
        command_line: str = "",
        commands: CommandsContainer = Provide[DiContainer.commands],
    ) -> None:
        """Parses and executes the command."""
        if not command_line:
            return

        command, args = self.parse_input(command_line)

        match command:
            case "help":
                commands.help().run()
            case "me" | "user":
                commands.user().run()
            case "liked:tracks" | "lt":
                commands.my_liked_tracks(args).run()
            case "me:followings":
                commands.followings(args).run()
            case "me:followings:tracks":
                commands.followings_tracks(args).run()
            case "me:tracks":
                commands.my_tracks(args).run()
            case "track":
                commands.track(args).run()
            case "track_streaming_url":
                commands.track_streaming_url(args).run()
            case "exit" | "quit" | "q":
                commands.exit().run()
            case _:
                commands.unknown_command().run()


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
