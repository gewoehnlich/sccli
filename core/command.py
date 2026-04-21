from core.action import Action
from core.resource import Resource


class Command:
    action: Action
    resource: Resource | None = None

    def __init__(
        self,
        action: Action,
        resource: Resource | None = None,
    ) -> None:
        self.action = action

        if resource:
            self.resource = resource

    def run(
        self,
    ) -> None:
        result = self.action.run()

        if self.resource:
            self.resource.print(data=result)
        else:
            print(result)
