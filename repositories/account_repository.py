from sqlalchemy import delete
from sqlalchemy.orm import Session
from models.account import Account


class AccountRepository:
    def __init__(
        self,
        session: Session
    ) -> None:
        self._session = session


    def get_by_client_id(
        self,
        client_id: str,
    ) -> Account | None:
        return self._session.get(Account, client_id)


    def create(
        self,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str,
        expire_timestamp: int,
    ) -> Account:
        account = Account(
            client_id        = client_id,
            client_secret    = client_secret,
            access_token     = access_token,
            refresh_token    = refresh_token,
            expire_timestamp = expire_timestamp,
        )

        self._session.add(instance = account)
        self._session.commit()

        return account

    def update(
        self,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str,
        expire_timestamp: int,
    ) -> Account:
        account = self._session.get(Account, client_id)

        if account is None:
            raise ValueError(f"Account {client_id} not found")

        account.client_secret = client_secret
        account.access_token = access_token
        account.refresh_token = refresh_token
        account.expire_timestamp = expire_timestamp

        self._session.commit()

        return account


    def delete(
        self,
        client_id: str,
    ) -> None:
        account = self._session.get(Account, client_id)

        if account is None:
            raise ValueError("Account not found")

        self._session.delete(account)
        self._session.commit()
