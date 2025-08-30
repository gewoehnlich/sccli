from dependency_injector.wiring import Provide, inject

from core.di_container import DiContainer
from core.command import process_command


@inject
def shell(di_container: DiContainer = Provide[DiContainer]) -> None:
    """Starts the interactive shell session."""
    di_container.commands().welcome_command()

    while True:
        try:
            command_line: str = input("sccli> ")
            process_command(command_line = command_line)

        except KeyboardInterrupt:
            di_container.commands().exit_command()
            break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
