from config import WELCOME_MESSAGE, EXIT_MESSAGE
from src.utils.command import process_command

def shell():
    """Starts the interactive shell session."""
    print(WELCOME_MESSAGE)
    
    while True:
        try:
            command_line = input("sccli> ")
            process_command(command_line)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(EXIT_MESSAGE)
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
