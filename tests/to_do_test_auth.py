from pathlib import Path
from dotenv import load_dotenv
import pytest

from config import TEST_TOKENS_FILE
from core.auth import Auth
from core.di_container import DiContainer


@pytest.fixture
def auth() -> Auth:
    load_dotenv()

    di_container: DiContainer = DiContainer()
    di_container.config.client_id.from_env(
        name = "CLIENT_ID",
        required = True,
        as_ = str,
    )

    di_container.config.client_secret.from_env(
        name = "CLIENT_SECRET",
        required = True,
        as_ = str,
    )

    di_container.config.redirect_uri.from_env(
        name = "REDIRECT_URI",
        default = "https://localhost:8080/callback",
        required = True,
        as_ = str,
    )

    di_container.config.tokens_file.from_value(TEST_TOKENS_FILE)

    di_container.wire(modules = [__name__])

    return di_container.auth(
        client_id              = di_container.config.client_id(),
        client_secret          = di_container.config.client_secret(),
        redirect_uri           = di_container.config.redirect_uri(),
        tokens_file            = di_container.config.tokens_file(),
        server                 = di_container.server(),
        authentication_request = di_container.requests().authentication,
        refresh_token_request  = di_container.requests().refresh_token,
    )


def test_if_tokens_file_is_created(
    auth: Auth
) -> None:
    file_exists: bool = Path(TEST_TOKENS_FILE).exists()
    assert file_exists is False

    access_token: str = auth.get_access_token()

    file_exists: bool = Path(TEST_TOKENS_FILE).exists()
    assert file_exists is True
