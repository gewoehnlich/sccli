import os
import base64
import hashlib
import time
import json
import asyncio
import webbrowser
from config import TOKENS_FILE
from src.utils.safe_getenv import safe_getenv
from src.utils.server import Server
from src.requests.refresh_token import RefreshTokenRequest
from src.requests.authentication import AuthenticationRequest
from typing import Any

class Auth:
    def __init__(self) -> None:
        self.client_id: str = safe_getenv("CLIENT_ID")
        self.client_secret: str = safe_getenv("CLIENT_SECRET")
        self.redirect_uri: str = safe_getenv("REDIRECT_URI")

    def get_access_token(self) -> str:
        access_token = self.load_token()
        if not access_token:
            access_token = self.authenticate_user()

        return access_token

    def load_token(self) -> str | None:
        try:
            with open(TOKENS_FILE, "r") as file:
                token_data = json.loads(file.read().strip())
                current_timestamp = int(time.time())
                expire_timestamp = (
                    int(token_data["timestamp"]) + 
                    int(token_data["expires_in"])
                )

            if current_timestamp > expire_timestamp - 100:
                if "refresh_token" not in token_data:
                    return None

                access_token = self.refresh_token(
                    token_data["refresh_token"]
                )
            else:
                access_token = token_data["access_token"]

            return access_token
        except (FileNotFoundError, KeyError):
            return None

    def refresh_token(self, refresh_token: str) -> str:
        response = RefreshTokenRequest(
            self.client_id,
            self.client_secret,
            refresh_token
        ).send()

        if not response:
            raise Exception("finish later. NO RESPONSE")

        try:
            token_data = response.json()
            token_data["timestamp"] = int(time.time()) 
        except Exception as e:
            raise e

        with open(TOKENS_FILE, "w") as file:
            file.write(json.dumps(token_data, indent=4))

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

        server = Server()
        webbrowser.open(auth_url)
        auth_code, returned_state = asyncio.run(server.run())
        if state != returned_state:
            raise Exception("State mismatch!")

        response = AuthenticationRequest(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            code_verifier,
            auth_code
        ).send()

        token_data = response.json()
        token_data["timestamp"] = int(time.time()) 

        with open(TOKENS_FILE, "w") as file:
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
