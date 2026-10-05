from pathlib import Path

from core.auth import Auth
from core.config import Config
from core.config_loader import ConfigLoader
from core.database import Database
from core.logger import Logger
from core.server import Server
from core.shell import Shell
from databases.sqlite_database import SqliteDatabase
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
from di.models_container import ModelsContainer
from di.repositories_container import RepositoriesContainer
from di.requests_container import RequestsContainer
from di.resources_container import ResourcesContainer
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
        )

        self.database: Database = SqliteDatabase(
            database_name=self.config.database.name,
        )

        self.models = ModelsContainer()

        self.repositories = RepositoriesContainer(
            session_factory=self.database.session_factory,
            models=self.models,
        )

        self.server: Server = HttpServer(
            port=self.config.server.port,
            path=self.config.server.path,
        )

        self.requests = RequestsContainer()

        self.auth = Auth(
            client_id=self.config.soundcloud.client_id,
            client_secret=self.config.soundcloud.client_secret,
            server=self.server,
            account_repository=self.repositories.account,
            authentication_request=self.requests.authentication,
            refresh_token_request=self.requests.refresh_token,
        )

        self.tasks = TasksContainer(
            auth=self.auth,
            requests=self.requests,
            repositories=self.repositories,
            messages=self.config.messages,
            server=self.server,
        )

        self.player = MpvPlayer(
            auth=self.auth,
            http_proxy=self.config.proxy.endpoint,
            logger=self.logger,
        )

        self.actions = ActionsContainer(
            auth=self.auth,
            requests=self.requests,
            repositories=self.repositories,
            messages=self.config.messages,
            tasks=self.tasks,
            player=self.player,
        )

        self.resources = ResourcesContainer()

        self.commands = CommandsContainer(
            actions=self.actions,
            resources=self.resources,
        )

        self.views = ViewsContainer()

        self.shell = Shell(
            commands=self.commands,
        )
