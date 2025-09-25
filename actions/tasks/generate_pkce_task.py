import base64
import hashlib
import os


class GeneratePkceTask(
    Task
):
    def run(
        self,
    ) -> tuple[str, str]:
        code_verifier: str = base64.urlsafe_b64encode(
            os.urandom(40)
        ).decode("utf-8").rstrip("=")

        code_challenge: str = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode("utf-8").rstrip("=")

        return code_verifier, code_challenge
