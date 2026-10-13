from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from di.repositories_container import RepositoriesContainer
from databases.sqlite_database import SqliteDatabase
from core.repository import Repository
from models.account import Account
from models.track import Track
from models.user import User


# --- test-only tables and repositories


class Base(DeclarativeBase):
    """Separate base, so test tables never end up in the real Model.metadata."""


class Widget(Base):
    __tablename__ = "widgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    color: Mapped[str | None]


class Gadget(Base):
    __tablename__ = "gadgets"

    code: Mapped[str] = mapped_column(primary_key=True)
    label: Mapped[str]


# Widget and Gadget are not subclasses of the project's Model, hence the ignores.
# Use the exact rule name your basedpyright reports for a bound violation.
class WidgetRepository(Repository[Widget]):  # pyright: ignore[reportInvalidTypeArguments]
    model = Widget


class GadgetRepository(Repository[Gadget]):  # pyright: ignore[reportInvalidTypeArguments]
    model = Gadget


# --- fixtures and helpers


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "app.db"


@pytest.fixture
def database(db_path: Path) -> Iterator[SqliteDatabase]:
    db = SqliteDatabase(path=db_path, alembic_config=AlembicConfig())

    with db.session() as session:
        Base.metadata.create_all(session.connection())

    yield db

    db.close()


@pytest.fixture
def widgets(database: SqliteDatabase) -> WidgetRepository:
    return WidgetRepository(database=database)


@pytest.fixture
def gadgets(database: SqliteDatabase) -> GadgetRepository:
    return GadgetRepository(database=database)


def count_rows(database: SqliteDatabase, model: type[Base]) -> int:
    with database.session() as session:
        return session.scalar(select(func.count()).select_from(model)) or 0


def find(repository: WidgetRepository, **filters: Any) -> Sequence[Widget]:
    # `get` is annotated `**kwargs: dict[str, Any]`, which type checkers read as
    # "every value is a dict". This helper keeps that out of the tests.
    return repository.get(**filters)


def seed(widgets: WidgetRepository) -> None:
    widgets.store(Widget(name="sprocket", color="red"))
    widgets.store(Widget(name="gear", color="red"))
    widgets.store(Widget(name="bolt", color="blue"))
    widgets.store(Widget(name="washer", color=None))


# --- get(): filtering rows


def test_get_without_filters_returns_every_row(widgets: WidgetRepository) -> None:
    seed(widgets)

    assert len(find(widgets)) == 4


def test_get_filters_by_a_column(widgets: WidgetRepository) -> None:
    seed(widgets)

    names = {widget.name for widget in find(widgets, color="red")}

    assert names == {"sprocket", "gear"}


def test_get_combines_filters_with_and(widgets: WidgetRepository) -> None:
    seed(widgets)

    found = find(widgets, color="red", name="gear")

    assert [widget.name for widget in found] == ["gear"]


def test_get_returns_nothing_when_no_row_matches(widgets: WidgetRepository) -> None:
    seed(widgets)

    assert len(find(widgets, color="green")) == 0


def test_get_with_none_matches_null_values(widgets: WidgetRepository) -> None:
    seed(widgets)

    found = find(widgets, color=None)

    assert [widget.name for widget in found] == ["washer"]


def test_get_with_an_unknown_column_raises(widgets: WidgetRepository) -> None:
    with pytest.raises(InvalidRequestError):
        find(widgets, colour="red")  # typo on purpose


def test_get_results_are_readable_after_the_session_closed(
    widgets: WidgetRepository,
) -> None:
    seed(widgets)

    found = find(widgets, name="bolt")

    # expire_on_commit=False: no DetachedInstanceError here
    assert found[0].color == "blue"


# --- get_one(): lookup by primary key


def test_get_one_finds_a_row_by_integer_key(widgets: WidgetRepository) -> None:
    stored = widgets.store(Widget(name="sprocket", color="red"))

    found = widgets.get_one(stored.id)

    assert found is not None
    assert found.name == "sprocket"


def test_get_one_finds_a_row_by_string_key(gadgets: GadgetRepository) -> None:
    gadgets.store(Gadget(code="g-1", label="first"))

    found = gadgets.get_one("g-1")

    assert found is not None
    assert found.label == "first"


def test_get_one_returns_none_for_a_missing_key(
    widgets: WidgetRepository,
    gadgets: GadgetRepository,
) -> None:
    assert widgets.get_one(999) is None
    assert gadgets.get_one("nope") is None


# --- store(): insert or update by primary key


def test_store_inserts_a_new_row_and_assigns_a_key(
    widgets: WidgetRepository,
    database: SqliteDatabase,
) -> None:
    stored = widgets.store(Widget(name="sprocket", color="red"))

    assert stored.id is not None
    assert stored.name == "sprocket"  # readable after the session closed
    assert count_rows(database, Widget) == 1


def test_store_returns_a_copy_and_leaves_the_argument_untouched(
    widgets: WidgetRepository,
) -> None:
    original = Widget(name="sprocket", color="red")

    stored = widgets.store(original)

    assert stored is not original
    assert original.id is None  # the key lands on the returned object


def test_store_updates_an_existing_row_without_duplicating_it(
    widgets: WidgetRepository,
    database: SqliteDatabase,
) -> None:
    stored = widgets.store(Widget(name="sprocket", color="red"))

    widgets.store(Widget(id=stored.id, name="cog", color="red"))

    assert count_rows(database, Widget) == 1
    updated = widgets.get_one(stored.id)
    assert updated is not None
    assert updated.name == "cog"


def test_store_inserts_then_updates_with_a_string_key(
    gadgets: GadgetRepository,
    database: SqliteDatabase,
) -> None:
    gadgets.store(Gadget(code="g-1", label="first"))
    gadgets.store(Gadget(code="g-1", label="renamed"))

    assert count_rows(database, Gadget) == 1
    found = gadgets.get_one("g-1")
    assert found is not None
    assert found.label == "renamed"


def test_store_keeps_stored_values_for_attributes_that_were_not_set(
    widgets: WidgetRepository,
) -> None:
    stored = widgets.store(Widget(name="sprocket", color="red"))

    widgets.store(Widget(id=stored.id, name="cog"))  # color not mentioned

    found = widgets.get_one(stored.id)
    assert found is not None
    assert found.color == "red"


def test_store_overwrites_a_value_with_an_explicit_none(
    widgets: WidgetRepository,
) -> None:
    stored = widgets.store(Widget(name="sprocket", color="red"))

    widgets.store(Widget(id=stored.id, name="cog", color=None))

    found = widgets.get_one(stored.id)
    assert found is not None
    assert found.color is None


def test_store_that_violates_a_constraint_raises_and_persists_nothing(
    widgets: WidgetRepository,
    database: SqliteDatabase,
) -> None:
    with pytest.raises(IntegrityError):
        widgets.store(Widget(name=None, color="red"))  # name is NOT NULL

    assert count_rows(database, Widget) == 0

    # and the database is still usable afterwards
    widgets.store(Widget(name="ok", color=None))
    assert count_rows(database, Widget) == 1


# --- delete()


def test_delete_removes_the_row(
    widgets: WidgetRepository,
    database: SqliteDatabase,
) -> None:
    stored = widgets.store(Widget(name="sprocket", color="red"))

    assert widgets.delete(stored) is True

    assert widgets.get_one(stored.id) is None
    assert count_rows(database, Widget) == 0


def test_delete_leaves_other_rows_alone(
    widgets: WidgetRepository,
    database: SqliteDatabase,
) -> None:
    seed(widgets)
    victim = find(widgets, name="bolt")[0]

    widgets.delete(victim)

    assert count_rows(database, Widget) == 3
    assert "bolt" not in {widget.name for widget in find(widgets)}


def test_delete_of_a_never_stored_object_raises(widgets: WidgetRepository) -> None:
    with pytest.raises(InvalidRequestError):
        widgets.delete(Widget(name="ghost", color=None))


# --- persistence and wiring


def test_data_survives_reopening_the_database(
    database: SqliteDatabase,
    widgets: WidgetRepository,
    db_path: Path,
) -> None:
    stored = widgets.store(Widget(name="persistent", color=None))
    database.close()

    reopened = SqliteDatabase(path=db_path, alembic_config=AlembicConfig())
    try:
        found = WidgetRepository(database=reopened).get_one(stored.id)
    finally:
        reopened.close()

    assert found is not None
    assert found.name == "persistent"


def test_each_project_repository_is_bound_to_its_model(
    database: SqliteDatabase,
) -> None:
    repositories = RepositoriesContainer(database=database)

    assert repositories.account.model is Account
    assert repositories.track.model is Track
    assert repositories.user.model is User
