from dependency_injector import containers, providers

from resources.json_resource import JsonResource
from resources.pprint_resource import PprintResource


class ResourcesContainer(
    containers.DeclarativeContainer
):
    json = providers.Singleton(
        JsonResource,
    )
    pprint = providers.Singleton(
        PprintResource,
    )
