from pathlib import Path

from alembic.config import Config as AlembicConfig
from dependency_injector import containers, providers

from core.auth import Auth
from core.config import Config
from core.config_loader import ConfigLoader
from core.database import Database
from core.http_client import HttpClient
from core.logger import Logger
from core.player import Player
from core.server import Server
from databases.sqlite_database import SqliteDatabase
from di.actions_container import ActionsContainer
from di.repositories_container import RepositoriesContainer
from players.mpv_player import MpvPlayer
from servers.http_server import HttpServer


class DiContainer(containers.DeclarativeContainer):
    config_file = providers.Dependency(instance_of=Path)

    config: providers.Singleton[Config] = providers.Singleton(
        ConfigLoader.load,
        path=config_file,
    )

    logger: providers.Singleton[Logger] = providers.Singleton(
        Logger,
        directory=config.provided.logs.directory,
        level=config.provided.logs.level,
    )

    database: providers.Singleton[Database] = providers.Singleton(
        SqliteDatabase,
        path=config.provided.database.path,
        alembic_config=providers.Singleton(
            AlembicConfig,
            file_=config.provided.database.alembic.ini,
            toml_file=config.provided.database.alembic.toml,
        ),
    )

    repositories: providers.Container[RepositoriesContainer] = (
        providers.Container(
            RepositoriesContainer,
            database=database,
        )
    )

    server: providers.Singleton[Server] = providers.Singleton(
        HttpServer,
        host=config.provided.server.host,
        port=config.provided.server.port,
        path=config.provided.server.path,
    )

    http_client: providers.Singleton[HttpClient] = providers.Singleton(
        HttpClient,
        proxy_endpoint=config.provided.proxy.endpoint,
    )

    auth: providers.Singleton[Auth] = providers.Singleton(
        Auth,
        _client_id=config.provided.soundcloud.client_id,
        _client_secret=config.provided.soundcloud.client_secret,
        _redirect_uri=config.provided.server.redirect_uri,
        _server=server,
        _account_repository=repositories().account,
        _http_client=http_client,
    )

    player: providers.Singleton[Player] = providers.Singleton(
        MpvPlayer,
        auth=auth,
        http_proxy=config.provided.proxy.endpoint,
        logger=logger,
    )

    actions: providers.Container[ActionsContainer] = providers.Container(
        ActionsContainer,
        auth=auth,
        http_client=http_client,
        repositories=repositories,
        logger=logger,
        player=player,
        messages=config.provided.messages,
    )
