from pathlib import Path

from alembic.config import Config as AlembicConfig

from core.auth import Auth
from core.config import Config
from core.config_loader import ConfigLoader
from core.database import Database
from core.logger import Logger
from core.server import Server
from databases.sqlite_database import SqliteDatabase
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
from di.repositories_container import RepositoriesContainer
from di.tasks_container import TasksContainer
from di.views_container import ViewsContainer
from players.mpv_player import MpvPlayer
from servers.http_server import HttpServer


class DiContainer:
    def __init__(
        self,
        config_file: Path,
    ) -> None:
        self.config: Config = ConfigLoader().load(
            path=config_file,
        )

        self.logger: Logger = Logger(
            directory=self.config.logs.directory,
            level=self.config.logs.level,
        )

        self.database: Database = SqliteDatabase(
            path=self.config.database.path,
            alembic_config=AlembicConfig(
                file_=self.config.database.alembic.ini,
                toml_file=self.config.database.alembic.toml,
            ),
        )

        self.repositories: RepositoriesContainer = RepositoriesContainer(
            database=self.database,
        )

        self.server: Server = HttpServer(
            host=self.config.server.host,
            port=self.config.server.port,
            path=self.config.server.path,
        )

        self.auth: Auth = Auth(
            client_id=self.config.soundcloud.client_id,
            client_secret=self.config.soundcloud.client_secret,
            redirect_uri=self.config.server.redirect_uri,
            server=self.server,
            account_repository=self.repositories.account,
        )

        self.player = MpvPlayer(
            auth=self.auth,
            http_proxy=self.config.proxy.endpoint,
            logger=self.logger,
        )

        self.tasks = TasksContainer(
            auth=self.auth,
            repositories=self.repositories,
            messages=self.config.messages,
        )

        self.actions = ActionsContainer(
            auth=self.auth,
            repositories=self.repositories,
            messages=self.config.messages,
            tasks=self.tasks,
            player=self.player,
        )

        self.commands = CommandsContainer(
            actions=self.actions,
        )

        self.views = ViewsContainer()
