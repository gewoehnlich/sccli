from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from databases.sqlite_database import SqliteDatabase

ENV_PY = """
from alembic import context
from sqlalchemy import create_engine, pool

config = context.config
url = config.get_main_option("sqlalchemy.url")
assert url is not None

engine = create_engine(url, poolclass=pool.NullPool)
with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=None)
    with context.begin_transaction():
        context.run_migrations()
"""

REVISION_HEADER = """
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
"""

CREATE_WIDGETS_REVISION = (
    REVISION_HEADER
    + """
def upgrade() -> None:
    op.create_table(
        "widgets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("widgets")
"""
)

BROKEN_REVISION = (
    REVISION_HEADER
    + """
def upgrade() -> None:
    raise RuntimeError("migration exploded")


def downgrade() -> None:
    pass
"""
)


def make_alembic_config(root: Path, revision_source: str) -> AlembicConfig:
    migrations = root / "migrations"
    versions = migrations / "versions"
    versions.mkdir(parents=True)

    (migrations / "env.py").write_text(ENV_PY, encoding="utf-8")
    (versions / "0001_init.py").write_text(revision_source, encoding="utf-8")

    config = AlembicConfig()
    config.set_main_option("script_location", str(migrations))

    return config


class Base(DeclarativeBase):
    pass


class Widget(Base):
    __tablename__ = "widgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)


# --- fixtures and helpers


@pytest.fixture
def alembic_config(tmp_path: Path) -> AlembicConfig:
    return make_alembic_config(tmp_path / "alembic", CREATE_WIDGETS_REVISION)


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "app.db"


@pytest.fixture
def database(
    db_path: Path, alembic_config: AlembicConfig
) -> Iterator[SqliteDatabase]:
    db = SqliteDatabase(path=db_path, alembic_config=alembic_config)
    yield db
    db.close()


def table_names(db: SqliteDatabase) -> set[str]:
    with db.session() as session:
        rows = session.execute(
            text("select name from sqlite_master where type = 'table'")
        ).scalars()

        return set(rows)


def insert_then_fail(db: SqliteDatabase) -> None:
    with db.session() as session:
        session.execute(text("insert into items (name) values ('x')"))

        raise RuntimeError("boom")


# --- engine and connection setup


def test_database_file_is_created_lazily(
    database: SqliteDatabase,
    db_path: Path,
) -> None:
    assert not db_path.exists()  # create_engine() does not connect

    table_names(database)

    assert db_path.exists()


def test_pragmas_are_applied_to_every_new_connection(
    database: SqliteDatabase,
) -> None:
    # two sessions open at once force two separate connections
    with database.session() as first, database.session() as second:
        for session in (first, second):
            foreign_keys = session.execute(
                text("PRAGMA foreign_keys")
            ).scalar_one()
            busy_timeout = session.execute(
                text("PRAGMA busy_timeout")
            ).scalar_one()

            assert foreign_keys == 1
            assert busy_timeout == 5000


# --- sessions


def test_session_commits_on_success(database: SqliteDatabase) -> None:
    with database.session() as session:
        session.execute(text("create table items (name text not null)"))
        session.execute(text("insert into items (name) values ('kept')"))

    with database.session() as session:
        names = session.execute(text("select name from items")).scalars().all()

    assert names == ["kept"]


def test_session_rolls_back_on_error(database: SqliteDatabase) -> None:
    with database.session() as session:
        session.execute(text("create table items (name text not null)"))

    with pytest.raises(RuntimeError, match="boom"):
        insert_then_fail(database)

    with database.session() as session:
        count = session.execute(text("select count(*) from items")).scalar_one()

    assert count == 0


def test_objects_stay_readable_after_the_session_closes(
    database: SqliteDatabase,
) -> None:
    database.run_migrations()

    with database.session() as session:
        widget = Widget(name="sprocket")
        session.add(widget)

    # expire_on_commit=False: no DetachedInstanceError on attribute access
    assert widget.name == "sprocket"
    assert widget.id is not None


def test_stored_objects_can_be_read_back(database: SqliteDatabase) -> None:
    database.run_migrations()

    with database.session() as session:
        session.add(Widget(name="gear"))

    with database.session() as session:
        names = (
            session.execute(text("SELECT name FROM widgets")).scalars().all()
        )

    assert names == ["gear"]


# --- migrations


def test_alembic_config_points_at_the_same_database(
    database: SqliteDatabase,
    alembic_config: AlembicConfig,
    db_path: Path,
) -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")

    assert url == f"sqlite+pysqlite:///{db_path}"


def test_run_migrations_creates_tables(database: SqliteDatabase) -> None:
    database.run_migrations()

    assert {"widgets", "alembic_version"} <= table_names(database)


def test_run_migrations_is_idempotent(database: SqliteDatabase) -> None:
    database.run_migrations()
    database.run_migrations()

    with database.session() as session:
        versions = (
            session.execute(text("select version_num from alembic_version"))
            .scalars()
            .all()
        )

    assert versions == ["0001"]


def test_failed_migration_propagates(
    tmp_path: Path,
    db_path: Path,
) -> None:
    broken = make_alembic_config(tmp_path / "broken", BROKEN_REVISION)
    db = SqliteDatabase(path=db_path, alembic_config=broken)

    with pytest.raises(RuntimeError, match="migration exploded"):
        db.run_migrations()

    assert "widgets" not in table_names(db)

    db.close()


# --- lifecycle and concurrency


def test_close_can_be_called_twice(database: SqliteDatabase) -> None:
    database.close()
    database.close()


def test_concurrent_writers_do_not_hit_database_is_locked(
    database: SqliteDatabase,
) -> None:
    with database.session() as session:
        session.execute(text("create table counter (n integer not null)"))

    def write_many() -> None:
        for _ in range(50):
            with database.session() as session:
                session.execute(text("insert into counter (n) values (1)"))

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(write_many) for _ in range(4)]

        for future in futures:
            future.result()  # re-raises any exception from the worker

    with database.session() as session:
        total = session.execute(
            text("select count(*) from counter")
        ).scalar_one()

    assert total == 200
