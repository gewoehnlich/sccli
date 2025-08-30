from dotenv import load_dotenv
from core.di_container import DiContainer
from core.shell import shell
from utils.safe_getenv import safe_getenv


def main() -> None:
    # load .env file variables
    load_dotenv()

    # dependency injection
    di_container: DiContainer = DiContainer()
    di_container.config.client_id     = safe_getenv("CLIENT_ID")
    di_container.config.client_secret = safe_getenv("CLIENT_SECRET")
    di_container.config.redirect_uri  = safe_getenv("REDIRECT_URI")
    di_container.config.tokens_file   = ".tokens.json"
    di_container.wire(modules = [__name__])

    # # cli music player
    # player: Player = Player()
    # player.run()

    # start shell session
    shell(di_container = di_container)

if __name__ == "__main__":
    main()
