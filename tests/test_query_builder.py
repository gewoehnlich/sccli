import pytest

from core.query_builder import QueryBuilder
from core.di_container import DiContainer


@pytest.fixture
def query_builder() -> QueryBuilder:
    """Return a fresh QueryBuilder with a test separator (',')."""
    return QueryBuilder(
        fields_separator = ", "
    )


def test_concatenate_fields(
    query_builder: QueryBuilder
) -> None:
    result = query_builder._concatenate_fields((
        "id", 
        "name", 
        "email"
    ))

    assert result == "id, name, email"


def test_concatenate_fields_trailing_separator(
    query_builder: QueryBuilder
) -> None:
    # It should not leave a trailing separator
    result = query_builder._concatenate_fields(("field1",))
    assert result == "field1"


def test_make_query_query(
    query_builder: QueryBuilder
) -> None:
    query = query_builder.make_query(
        statement = "INSERT INTO",
        table = "users",
        fields = ("id", "name"),
    )
    assert query == "INSERT INTO users(id, name)"


def test_fields_separator_changes(query_builder: QueryBuilder):
    qb = QueryBuilder(fields_separator=" | ")
    query = qb.make_query("SELECT", "users", ("id", "name"))
    assert query == "SELECT users(id | name)"


# --- Integration test using DI container ---
def test_query_builder_from_container():
    container = DiContainer()
    container.config.fields_separator.from_value(";")

    qb: QueryBuilder = container.query_builder()

    query = qb.make_query("INSERT INTO", "users", ("id", "name"))
    assert query == "INSERT INTO users(id;name)"
