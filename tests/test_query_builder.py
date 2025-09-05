import pytest

from core.query_builder import QueryBuilder
from core.di_container import DiContainer


@pytest.fixture
def qb() -> QueryBuilder:
    """Return a fresh QueryBuilder with a test separator (',')."""
    return QueryBuilder()


def test_concatenate_fields(
    qb: QueryBuilder
) -> None:
    result = qb._concatenate_fields((
        "id", 
        "name", 
        "email"
    ))

    assert result == "id, name, email"


def test_concatenate_fields_trailing_separator(
    qb: QueryBuilder
) -> None:
    # It should not leave a trailing separator
    result = qb._concatenate_fields(("field1",))
    assert result == "field1"


def test_make_query(
    qb: QueryBuilder
) -> None:
    query = qb.make_query(
        statement = "INSERT INTO",
        table = "users",
        fields = ("id", "name"),
    )
    assert query == "INSERT INTO users(id, name)"


def test_is_singleton(
    qb: QueryBuilder
) -> None:
    qb2: QueryBuilder = QueryBuilder()

    assert qb == qb2


def test_query_builder_from_container():
    container = DiContainer()

    qb: QueryBuilder = container.query_builder().query_builder()

    query = qb.make_query(
        statement = "INSERT INTO",
        table = "users",
        fields = ("id", "name"),
    )

    assert query == "INSERT INTO users(id, name)"
