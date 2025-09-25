import base64
import os


class GenerateStateTask(
    Task
):
    def run(
        self,
    ) -> str:
        state: str = base64.urlsafe_b64encode(
            os.urandom(16)
        ).decode().rstrip("=")

        return state
