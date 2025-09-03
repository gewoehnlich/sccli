from core.action import Action
from core.resource import Resource


class Command:
    action: Action
    resource: Resource

    def run(
        action: Action,
        resource: Resource,
    ) -> None:
        if self.action:
            result = self.action()

        if result and self.resource:
            response = self.resource(result)
