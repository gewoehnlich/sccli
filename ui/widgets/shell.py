import shlex
from typing import Any

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, RichLog

from di.commands_container import CommandsContainer


class Shell(Vertical):
    DEFAULT_CSS = """
    Shell {
        height: 100%;
    }
    Shell > RichLog {
        height: 1fr;
    }
    Shell > Input {
        height: 3;
    }
    """

    def __init__(
        self,
        commands: CommandsContainer,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.commands = commands

    def compose(self) -> ComposeResult:
        yield RichLog(
            id="shell-output",
            markup=True,
            wrap=True,
        )
        yield Input(
            placeholder="sccli> ",
            id="shell-input",
        )

    def on_mount(
        self,
    ) -> None:
        self.commands.welcome.run(
            output=self.write,
        )
        self.query_one(Input).focus()

    def write(
        self,
        text: str,
    ) -> None:
        self.query_one(RichLog).write(text)

    def on_input_submitted(
        self,
        event: Input.Submitted,
    ) -> None:
        event.stop()

        command_line = event.value.strip()
        event.input.clear()

        if not command_line:
            return

        self.write(f"[b]sccli>[/b] {command_line}")
        self.process_command(command_line)

    def process_command(
        self,
        command_line: str,
    ) -> None:
        try:
            command, _args = self._parse_input(command_line)
        except ValueError:  # e.g. unbalanced quotes
            self.write("[red]Could not parse the command[/red]")
            return

        match command:
            case "help":
                self.commands.help.run(
                    output=self.write,
                )
            case "liked:tracks" | "lt":
                self.commands.liked_tracks.run(
                    output=self.write,
                )
            case "track:play" | "tp":
                self.commands.play.run(
                    output=self.write,
                )
            case "exit" | "quit" | "q":
                print(123)
                #
                # self.app.exit()
            case _:
                self.commands.unknown.run(
                    output=self.write,
                )

    @staticmethod
    def _parse_input(
        command_line: str,
    ) -> tuple[str, list[str]]:
        parts = shlex.split(command_line)

        return parts[0].lower(), parts[1:]
