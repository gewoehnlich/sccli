from core.settings import Settings
from default_settings.app import AppSettings
from core.di_container import DiContainer


@pytest.fixture
def container() -> DiContainer:
    settings: AppSettings = Settings().load()

    di_container: DiContainer = DiContainer()
    di_container.config.from_pydantic(
        settings = settings,
    )

    di_container.database().initialize_tables()

    di_container.wire(
        modules = [__name__],
    )

    return di_container


def test_get_access_token() -> None:
    pass
