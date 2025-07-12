from src.commands.exit import exit_command
from src.commands.welcome import welcome_command
from src.utils.command import process_command

def shell() -> None:
    """Starts the interactive shell session."""
    welcome_command()
    
    while True:
        try:
            command_line: str = input("sccli> ")
            process_command(command_line)
        except KeyboardInterrupt:
            exit_command()
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
