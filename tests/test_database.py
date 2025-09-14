from pathlib import Path
import os
import pytest

from core.database import Database
from core.di_container import DiContainer
from core.table import Table
from default_settings.app import AppSettings
from di.tables_container import TablesContainer


@pytest.fixture
def db() -> Database:
    settings: AppSettings = Settings().load()

    di_container: DiContainer = DiContainer()
    di_container.config.from_pydantic(settings)

    di_container.wire(modules = [__name__])

    return di_container.db()


def check_if_table_exists(
    db: Database,
    table: Table,
) -> bool:
    query: str = f"""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?;
    """

    db.cursor.execute(query, (table.name,))
    table_exists = db.cursor.fetchone() is not None

    return table_exists


def test_if_db_created(
    db: Database
) -> None:
    db_filepath: Path = Path(TEST_DATABASE_NAME)

    assert db_filepath.exists()


def test_if_initial_tables_are_created(
    db: Database
) -> None:
    for name, provider in db.tables.providers.items():
        table: Table = provider()

        table_exists: bool = check_if_table_exists(
            db = db,
            table = table,
        )

        assert table_exists == False

    db.initialize_tables()

    for name, provider in db.tables.providers.items():
        table: Table = provider()

        table_exists: bool = check_if_table_exists(
            db = db,
            table = table,
        )

        assert table_exists == True


def test_create_table_if_not_exists(
    db: Database
) -> None:
    test_table: Table = Table()
    test_table.name = "test"
    test_table.fields = ("id", "name")

    table_exists = check_if_table_exists(
        db = db,
        table = test_table
    )

    assert table_exists is False

    db.create_table_if_not_exists(table = test_table)

    table_exists = check_if_table_exists(
        db = db,
        table = test_table
    )

    assert table_exists is True

def test_if_test_db_deleted_after_tests(
    db: Database
) -> None:
    db_exists: bool = Path(TEST_DATABASE_NAME).exists()
    assert db_exists == True

    db._db.close()
    os.remove(TEST_DATABASE_NAME)

    db_exists = Path(TEST_DATABASE_NAME).exists()
    assert db_exists == False
