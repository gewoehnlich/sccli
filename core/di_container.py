from api_requests.authentication_request import AuthenticationRequest
from api_requests.refresh_token_request import RefreshTokenRequest
from core.auth import Auth
from core.config import Config
from core.database import Database
from core.server import Server
from databases.sqlite_database import SqliteDatabase
from default_settings.app import AppSettings
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
from di.dto_container import DtoContainer
from di.models_container import ModelsContainer
from di.repository_container import RepositoryContainer
from di.requests_container import RequestsContainer
from di.resources_container import ResourcesContainer


class DiContainer:
    config: AppSettings = Config().load()

    database: Database = SqliteDatabase(
        database_name=config.database.name,
        models=ModelsContainer(),
    )

    repositories = RepositoryContainer(
        session_factory=database.session_factory,
    )

    auth = Auth(
        client_id=config.soundcloud.client_id,
        client_secret=config.soundcloud.client_secret,
        server=Server(
            port=config.server.port,
            path=config.server.path,
        ),
        account_repository=repositories.account,
        authentication_request=AuthenticationRequest,
        refresh_token_request=RefreshTokenRequest,
    )

    dto = DtoContainer()

    requests = RequestsContainer()

    actions = ActionsContainer(
        auth=auth,
        requests=requests,
        repositories=repositories,
        messages=config.messages,
    )

    resources = ResourcesContainer()

    commands = CommandsContainer(
        actions=actions,
        resources=resources,
    )
