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

    di_container.wire(modules = [__name__])

    # # cli music player
    # player: Player = Player()
    # player.run()

    # start shell session
    shell: Shell = Shell()
    shell.run()

if __name__ == "__main__":
    main()
