from core.action import Action


class Command:
    action: Action | None = None
    resource: Resource | None = None

    def run(
        action: Action,
        resource: Resource,
    ) -> None:
        if self.action:
            result = self.action()

        if result and self.resource:
            response = self.resource(result)
