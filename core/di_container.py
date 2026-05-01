from core.auth import Auth
from core.config import Config
from core.database import Database
from core.logger import Logger
from core.server import Server
from core.settings import Settings
from core.shell import Shell
from databases.sqlite_database import SqliteDatabase
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
from di.models_container import ModelsContainer
from di.repository_container import RepositoryContainer
from di.requests_container import RequestsContainer
from di.resources_container import ResourcesContainer
from di.tasks_container import TasksContainer
from players.mpv_player import MpvPlayer
from servers.http_server import HttpServer
from ui.app import App
from views.track_view import TrackView


class DiContainer:
    config: Settings = Config().load()

    logger = Logger()

    database: Database = SqliteDatabase(
        database_name=config.database.name,
    )

    models = ModelsContainer()

    repositories = RepositoryContainer(
        session_factory=database.session_factory,
        models=models,
    )

    server: Server = HttpServer(
        port=config.server.port,
        path=config.server.path,
    )

    requests = RequestsContainer()

    auth = Auth(
        client_id=config.soundcloud.client_id,
        client_secret=config.soundcloud.client_secret,
        server=server,
        account_repository=repositories.account,
        authentication_request=requests.authentication,
        refresh_token_request=requests.refresh_token,
    )

    tasks = TasksContainer(
        auth=auth,
        requests=requests,
        repositories=repositories,
        messages=config.messages,
        server=server,
    )

    actions = ActionsContainer(
        auth=auth,
        requests=requests,
        repositories=repositories,
        messages=config.messages,
        tasks=tasks,
    )

    resources = ResourcesContainer()

    commands = CommandsContainer(
        actions=actions,
        resources=resources,
    )

    player = MpvPlayer(
        player="mpv",
        auth=auth,
    )

    shell = Shell(
        commands=commands,
    )

    app = App(
        track_repository=repositories.track,
        logger=logger,
        track_view=TrackView(
            fields=['urn', 'title', 'duration']
        ),
    )
