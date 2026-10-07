from config.base_config_model import BaseConfigModel


class MessagesConfig(BaseConfigModel):
    welcome: str = (
        "Welcome to the sccli interactive shell!\n"
        "Type 'help' for a list of available commands.\n"
    )
    exit: str = "exiting.\n"
    help: str = (
        "\nAvailable commands:\n"
        "  search <query> - Search for something on SoundCloud.\n"
        "  token          - Display the current access token.\n"
        "  help           - Show this help message.\n"
        "  exit, quit     - Exit the shell.\n"
    )
    unknown: str = (
        "Unknown command.\n"
        "Type 'help' for a list of available commands.\n"
    )
