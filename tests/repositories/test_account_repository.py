import pytest

from core.di_container import DiContainer


@pytest.fixture
def container() -> DiContainer:
    container = DiContainer(
        config={
            "finder": {
                "type": "csv",
                "csv": {
                    "path": "/fake-movies.csv",
                    "delimiter": ",",
                },
                "sqlite": {
                    "path": "/fake-movies.db",
                },
            },
        },
    )
    return container
