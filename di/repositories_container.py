from core.database import Database
from repositories.account_repository import AccountRepository
from repositories.image_repository import ImageRepository
from repositories.setting_repository import SettingRepository
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


from dependency_injector import containers, providers


class RepositoriesContainer(containers.DeclarativeContainer):
    database = providers.Dependency(instance_of=Database)

    account: providers.Singleton[AccountRepository] = providers.Singleton(
        AccountRepository, database=database,
    )
    track: providers.Singleton[TrackRepository] = providers.Singleton(
        TrackRepository, database=database,
    )
    user: providers.Singleton[UserRepository] = providers.Singleton(
        UserRepository, database=database,
    )
    image: providers.Singleton[ImageRepository] = providers.Singleton(
        ImageRepository, database=database,
    )
    setting: providers.Singleton[SettingRepository] = providers.Singleton(
        SettingRepository, database=database,
    )
