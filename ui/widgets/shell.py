import shlex
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Input, RichLog

from di.commands_container import CommandsContainer


class Shell(Vertical):
    def __init__(
        self,
        commands: CommandsContainer,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.commands = commands

    def compose(self) -> ComposeResult:
        with Container(id="shell-container"):
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
        self.styles.height = "100%"

        container = self.query_one(Container)
        container.styles.padding = 1

        rich_log = self.query_one(RichLog)
        rich_log.styles.width = "100%"
        rich_log.styles.height = "1fr"
        rich_log.styles.padding = (1, 2)
        rich_log.styles.margin = 1

        input_widget = self.query_one(Input)
        input_widget.styles.width = "100%"
        input_widget.styles.height = 3
        input_widget.focus()

        self.commands.welcome.run(
            output=self.write,
        )

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

        self.write(f"[plum2]sccli>[/plum2] [thistle1]{command_line}[/thistle1]")
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
                self.write("exit")
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
