from pathlib import Path
import pytest

from _config.database import TEST_DATABASE_NAME
from core.database import Database
from core.di_container import DiContainer
from core.table import Table
from di.tables_container import TablesContainer


@pytest.fixture
def db() -> Database:
    di_container: DiContainer = DiContainer()
    di_container.config.database_name.from_value(TEST_DATABASE_NAME)

    di_container.wire(modules = [__name__])

    return di_container.db()


def test_if_db_created(
    db: Database
) -> None:
    db_filepath: Path = Path(TEST_DATABASE_NAME)

    assert db_filepath.exists()


def test_if_initial_tables_are_created(
    db: Database
) -> None:
    # to-do 
    db.initialize_tables()
    pass


def test_create_table_if_not_exists(
    db: Database
) -> None:
    test_table: Table = Table()
    test_table.name = "test"
    test_table.fields = ("id", "name")

    db.create_table_if_not_exists(table = test_table)
    pass
