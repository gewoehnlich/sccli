from dependency_injector import providers
from core.table import Table


class Model:
    db:  Table
    dto: providers.Dependency
