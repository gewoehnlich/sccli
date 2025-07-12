import shlex
from src.core.auth import Auth

def process_command(command_line: str):
    """Parses and executes a single command."""
    if not command_line:
        return

    # Use shlex.split to handle quoted arguments correctly
    parts = shlex.split(command_line)
    command = parts[0].lower()
    args = parts[1:]
    auth_instance = Auth()

    if command == "search":
        if not args:
            print("Error: The 'search' command requires a query.")
            print("Usage: search <your query>")
            return
        query = " ".join(args)
        print(f"Searching for '{query}'...")
        # access_token = auth_instance.get_access_token()
        # Here you would call your search logic with the access token and query
        # e.g., soundcloud_client.search(query, token=access_token)

    elif command == "token":
        print("Fetching access token...")
        access_token = auth_instance.get_access_token()
        print(f"Access Token: {access_token}")

    elif command == "help":
        print("\nAvailable commands:")
        print("  search <query> - Search for something on SoundCloud.")
        print("  token          - Display the current access token.")
        print("  help           - Show this help message.")
        print("  exit, quit     - Exit the shell.")
        print()

    else:
        print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")
