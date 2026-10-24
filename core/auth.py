import base64
import hashlib
import os
import secrets
import time
import webbrowser
from typing import Any

from core.http_client import HttpClient
from core.request import Request
from core.server import Server
from exceptions.auth.authorization_denied_error import AuthorizationDeniedError
from exceptions.auth.state_mismatch_error import StateMismatchError
from models.account import Account
from repositories.account_repository import AccountRepository


class Auth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        server: Server,
        account_repository: AccountRepository,
        http_client: HttpClient,
    ) -> None:
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_uri: str = redirect_uri

        self._server: Server = server
        self._account_repository: AccountRepository = account_repository
        self._http_client: HttpClient = http_client

    def get_access_token(
        self,
    ) -> str:
        account: Account | None = self._account_repository.get_one(
            primary_key=self._client_id,
        )

        if not account:
            account = self._authenticate_user()

        current_timestamp = int(time.time())
        if current_timestamp > account.expire_timestamp - 100:
            account = self._refresh_token(
                account=account,
            )

        assert account is not None

        return account.access_token

    def _authenticate_user(
        self,
    ) -> Account:
        code_verifier, code_challenge = self._generate_pkce()
        state = self._generate_state()

        auth_url: str = Request(
            method=Request.METHOD.GET,
            url=Request.URL.AUTHORIZATION,
            data={
                "client_id": self._client_id,
                "redirect_uri": self._redirect_uri,
                "response_type": "code",
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
                "state": state,
            },
        ).build_url()

        self._server.start()

        try:
            if not webbrowser.open(auth_url):
                print(f"Open this URL in your browser:\n{auth_url}")

            result = self._server.wait_for_callback(timeout=300)
        finally:
            self._server.stop()

        if result.error is not None:
            raise AuthorizationDeniedError(result.error)

        if (
            result.code is None
            or result.state is None
            or not secrets.compare_digest(result.state.encode(), state.encode())
        ):
            raise StateMismatchError

        auth_code: str = result.code

        request: Request = Request(
            method=Request.METHOD.POST,
            url=Request.URL.TOKEN,
            data={
                "grant_type": "authorization_code",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "redirect_uri": self._redirect_uri,
                "code_verifier": code_verifier,
                "code": auth_code,
            },
        )

        response: dict[str, Any] = self._http_client.send(request)

        account: Account = self._account_repository.store(
            model=Account(
                client_id=self._client_id,
                client_secret=self._client_secret,
                access_token=str(response["access_token"]),
                refresh_token=str(response["refresh_token"]),
                expire_timestamp=int(time.time()) + int(response["expires_in"]),
            ),
        )

        return account

    def _refresh_token(
        self,
        account: Account,
    ) -> Account:
        request: Request = Request(
            method=Request.METHOD.POST,
            url=Request.URL.REFRESH_TOKEN,
            data={
                "grant_type": "refresh_token",
                "client_id": account.client_id,
                "client_secret": account.client_secret,
                "refresh_token": account.refresh_token,
            },
        )

        response: dict[str, Any] = self._http_client.send(request)

        updated_account: Account = self._account_repository.store(
            model=Account(
                client_id=account.client_id,
                client_secret=account.client_secret,
                access_token=str(response["access_token"]),
                refresh_token=str(response["refresh_token"]),
                expire_timestamp=int(time.time()) + int(response["expires_in"]),
            ),
        )

        return updated_account

    def _generate_pkce(self) -> tuple[str, str]:
        code_verifier: str = (
            base64.urlsafe_b64encode(
                os.urandom(40),
            )
            .decode("utf-8")
            .rstrip("=")
        )

        code_challenge: str = (
            base64.urlsafe_b64encode(
                hashlib.sha256(
                    code_verifier.encode(),
                ).digest()
            )
            .decode("utf-8")
            .rstrip("=")
        )

        return code_verifier, code_challenge

    def _generate_state(self) -> str:
        state: str = (
            base64.urlsafe_b64encode(
                os.urandom(16),
            )
            .decode()
            .rstrip("=")
        )

        return state
