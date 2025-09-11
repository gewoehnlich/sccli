# to-do: add config validator running before the main script

# [DATABASE]
DATABASE_NAME: str = "sccli.db"
TEST_DATABASE_NAME: str = "test.db"


# [MESSAGES]
WELCOME_COMMAND_MESSAGE: str = (
    "welcome to the sccli interactive shell.\n"
    "type 'help' for a list of available commands.\n"
)
EXIT_COMMAND_MESSAGE: str = "exiting.\n"
HELP_COMMAND_MESSAGE: str = (
    "\nAvailable commands:\n"
    "  search <query> - Search for something on SoundCloud.\n"
    "  token          - Display the current access token.\n"
    "  help           - Show this help message.\n"
    "  exit, quit     - Exit the shell.\n"
)
UNKNOWN_COMMAND_MESSAGE: str = (
    "Unknown command.\n"
    "Type 'help' for a list of commands.\n"
)


# [SERVER]
SERVER_PORT: int = 8080
SERVER_PATH: str = "/callback"


# [TOKENS]
TOKENS_FILE: str      = ".tokens.json"
TEST_TOKENS_FILE: str = ".test_tokens.json"
