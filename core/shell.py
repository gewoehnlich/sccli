from commands.exit_command import exit_command
from commands.welcome_command import welcome_command
from core.command import process_command

def shell() -> None:
    """Starts the interactive shell session."""
    welcome_command()
    
    while True:
        try:
            command_line: str = input("sccli> ")
            process_command(command_line = command_line)

        except KeyboardInterrupt:
            exit_command()
            break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
