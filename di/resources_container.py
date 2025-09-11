from dependency_injector import containers, providers

from resources.pprint_resource import PprintResource


class ResourcesContainer(containers.DeclarativeContainer):
    pprint = providers.Singleton(PprintResource)
