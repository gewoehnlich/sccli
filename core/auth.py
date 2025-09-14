import os
import base64
import hashlib
import time
import json
import asyncio
import webbrowser
from typing import Any, Self
from requests import Response

from core.request import Request
from core.server import Server
from di.auth_requests import AuthRequestsContainer


class Auth:
    _instance:    Self | None = None
    _initialized: bool        = False

    def __new__(
        cls: type[Self],
        *args, 
        **kwargs,
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(
        self,
        client_id: str,
        client_secret: str,
        server_port: int,
        server_path: str,
        tokens_file: str,
        server: Server,
        auth_requests: AuthRequestsContainer,
    ) -> None:
        if self._initialized:
            return

        self.client_id: str     = client_id
        self.client_secret: str = client_secret
        self.redirect_uri: str  = f"http://localhost:{server_port}{server_path}"
        self.tokens_file: str   = tokens_file

        self.server: Server = server

        self.authentication_request: Request = auth_requests.authentication
        self.refresh_token_request:  Request = auth_requests.refresh_token

        self._initialized = True


    def get_access_token(self) -> str:
        access_token = self.load_token()

        if not access_token:
            access_token = self.authenticate_user()

        return access_token


    def load_token(self) -> str | None:
        try:
            with open(
                file = self.tokens_file,
                mode = "r",
                encoding = "utf-8",
            ) as file:
                token_data = json.loads(
                    file.read().strip()
                )

                current_timestamp = int(time.time())
                expire_timestamp = (
                    int(token_data["timestamp"]) + int(token_data["expires_in"])
                )

            if current_timestamp > expire_timestamp - 100:
                if "refresh_token" not in token_data:
                    return None

                access_token = self.refresh_token(
                    refresh_token = token_data["refresh_token"]
                )

            else:
                access_token = token_data["access_token"]

            return access_token

        except (FileNotFoundError, KeyError):
            return None


    def refresh_token(
        self,
        refresh_token: str
    ) -> str:
        print(type(self.refresh_token_request))
        response: Response = self.refresh_token_request(
            client_id      = self.client_id,
            client_secret  = self.client_secret,
            refresh_token  = refresh_token
        ).send()

        if not response:
            raise Exception("finish later. NO RESPONSE")

        try:
            token_data = response.json()
            token_data["timestamp"] = int(time.time())

        except Exception as e:
            raise e

        with open(
            file = self.tokens_file,
            mode = "w",
            encoding = "utf-8",
        ) as file:
            file.write(
                json.dumps(token_data, indent=4)
            )

        access_token: Any = token_data.get("access_token")
        if not isinstance(access_token, str):
            raise ValueError("access_token is not a string.")

        return access_token


    def authenticate_user(self) -> str:
        code_verifier, code_challenge = self.generate_pkce()
        state = self.generate_state()

        auth_url = (
            "https://secure.soundcloud.com/authorize"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            "&response_type=code"
            f"&code_challenge={code_challenge}"
            "&code_challenge_method=S256"
            f"&state={state}"
        )

        webbrowser.open(auth_url)
        auth_code, returned_state = asyncio.run(self.server.run())
        if state != returned_state:
            raise Exception("State mismatch!")

        response = self.authentication_request(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            code_verifier,
            auth_code
        ).send()

        token_data: dict[str, Any] = response.json()
        token_data["timestamp"] = int(time.time())

        with open(
            file = self.tokens_file,
            mode = "w",
            encoding = "utf-8",
        ) as file:
            file.write(json.dumps(token_data, indent=4))

        access_token: Any = token_data.get("access_token")
        if not isinstance(access_token, str):
            raise ValueError("access_token is not a string.")

        return access_token


    def generate_pkce(self) -> tuple[str, str]:
        code_verifier: str = base64.urlsafe_b64encode(
            os.urandom(40)
        ).decode("utf-8").rstrip("=")
        code_challenge: str = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode("utf-8").rstrip("=")

        return code_verifier, code_challenge


    def generate_state(self) -> str:
        state: str = base64.urlsafe_b64encode(
            os.urandom(16)
        ).decode().rstrip("=")

        return state
