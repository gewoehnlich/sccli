import os
import base64
import hashlib
import time
import json
import asyncio
import webbrowser
from typing import Any, Self
from rich import inspect
from rich.pretty import pprint

from core.database import Database
from core.dto import Dto
from core.request import Request
from core.resource import Resource
from core.server import Server
from models.account import Account
from repositories.account_repository import AccountRepository


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
        server: Server,
        database: Database,
        authentication_request: Request,
        refresh_token_request: Request,
    ) -> None:
        if self._initialized:
            return

        self.client_id:     str = client_id
        self.client_secret: str = client_secret
        self.redirect_uri:  str = f"http://localhost:{ server.port }{ server.path }"

        self.server: Server = server
        self.database: Database = database

        self.authentication_request: Request = authentication_request
        self.refresh_token_request:  Request = refresh_token_request

        self._initialized = True


    def get_access_token(
        self,
    ) -> str:
        with self.database.session_factory() as session:
            account: Account | None = AccountRepository(session).get_by_client_id(
                client_id = self.client_id,
            )

        if not account:
            return self.__authenticate_user()

        current_timestamp = int(time.time())
        if current_timestamp > account.expire_timestamp - 100:
            return self.__refresh_token(
                account = account,
            )

        return account.access_token


    def __refresh_token(
        self,
        account: Account,
    ) -> str:
        request: Request = self.refresh_token_request(
            client_id      = account.client_id,
            client_secret  = account.client_secret,
            refresh_token  = account.refresh_token,
        )

        response: dict[str, Any] = request.send()

        with self.database.session_factory() as session:
            account: Account = AccountRepository(session).update(
                client_id = self.client_id,
                client_secret = self.client_secret,
                access_token = str(response["access_token"]),
                refresh_token = str(response["refresh_token"]),
                expire_timestamp = int(time.time()) + int(response["expires_in"]),
            )

        return account.access_token


    def __authenticate_user(
        self,
    ) -> str:
        code_verifier, code_challenge = self.__generate_pkce()
        state = self.__generate_state()

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

        request: Request = self.authentication_request(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            code_verifier,
            auth_code
        )

        response: dict[str, Any] = request.send()

        with self.database.session_factory() as session:
            account: Account = AccountRepository(session).create(
                client_id = self.client_id,
                client_secret = self.client_secret,
                access_token = str(response["access_token"]),
                refresh_token = str(response["refresh_token"]),
                expire_timestamp = int(time.time()) + int(response["expires_in"]),
            )

        return account.access_token


    def __generate_pkce(self) -> tuple[str, str]:
        code_verifier: str = base64.urlsafe_b64encode(
            os.urandom(40)
        ).decode("utf-8").rstrip("=")

        code_challenge: str = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode("utf-8").rstrip("=")

        return code_verifier, code_challenge


    def __generate_state(self) -> str:
        state: str = base64.urlsafe_b64encode(
            os.urandom(16)
        ).decode().rstrip("=")

        return state
