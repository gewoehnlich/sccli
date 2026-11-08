from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


class Database:
    def __init__(
        self,
        engine: AsyncEngine,
        alembic_config: AlembicConfig,
        migrations_url: str,
    ) -> None:
        self._engine: AsyncEngine = engine

        self._sessions: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )

        alembic_config.set_main_option("sqlalchemy.url", migrations_url)
        self._alembic_config: AlembicConfig = alembic_config

    def run_migrations(self) -> None:
        command.upgrade(self._alembic_config, "head")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with self._sessions.begin() as session:
            yield session

    async def close(self) -> None:
        await self._engine.dispose()
