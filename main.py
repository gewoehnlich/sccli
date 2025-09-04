from _config.messages import EXIT_COMMAND_MESSAGE, HELP_COMMAND_MESSAGE, UNKNOWN_COMMAND_MESSAGE, WELCOME_COMMAND_MESSAGE
from _config.server import SERVER_PORT, SERVER_PATH
from dotenv import load_dotenv
from core.di_container import DiContainer
from core.shell import Shell


def main() -> None:
    # load .env file variables
    load_dotenv()

    # dependency injection
    di_container: DiContainer = DiContainer()

    di_container.config.client_id.from_env(
        name = "CLIENT_ID",
        required = True,
    )

    di_container.config.client_secret.from_env(
        name = "CLIENT_SECRET",
        required = True,
    )

    di_container.config.redirect_uri.from_env(
        name = "REDIRECT_URI",
        default = "https://localhost:8080/callback",
        required = True,
    )

    di_container.config.tokens_file.from_env(
        name = "TOKENS_FILE",
        default = ".tokens.json",
        required = True,
    )

    di_container.config.server_port.from_value(SERVER_PORT)
    di_container.config.server_path.from_value(SERVER_PATH)

    di_container.config.welcome_command_message.from_value(
        WELCOME_COMMAND_MESSAGE
    )

    di_container.config.exit_command_message.from_value(
        EXIT_COMMAND_MESSAGE
    )

    di_container.config.help_command_message.from_value(
        HELP_COMMAND_MESSAGE
    )

    di_container.config.unknown_command_message.from_value(
        UNKNOWN_COMMAND_MESSAGE
    )

    di_container.wire(modules = [__name__])

    # # cli music player
    # player: Player = Player()
    # player.run()

    # start shell session
    shell: Shell = Shell()
    shell.run()

if __name__ == "__main__":
    main()
