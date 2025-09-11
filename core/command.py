from core.action import Action
from core.resource import Resource


class Command:
    action: Action
    resource: Resource

    def __init__(
        self,
        action: Action,
        resource: Resource,
    ) -> None:
        if action:
            self.action = action

        if resource:
            self.resource = resource

    def run(self) -> None:
        if self.action:
            result = self.action().run()

        if result and self.resource:
            response = self.resource(result)
