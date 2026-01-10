from core.database import Database
from models.account import Account


class AccountRepository:
    database: Database


    def __init__(
        self,
        database: Database
    ) -> None:
        self.database = database


    def get(
        self,
        client_id: str,
    ) -> Account | None:
        with self.database.session_factory() as session:
            return session.get(Account, client_id)


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

        with self.database.session_factory() as session:
            session.add(instance = account)
            session.commit()

        return account


    def update(
        self,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str,
        expire_timestamp: int,
    ) -> Account:
        with self.database.session_factory() as session:
            account = session.get(Account, client_id)

            if account is None:
                raise ValueError(f"Account { client_id } not found")

            account.client_secret    = client_secret
            account.access_token     = access_token
            account.refresh_token    = refresh_token
            account.expire_timestamp = expire_timestamp

            session.commit()

        return account


    def delete(
        self,
        client_id: str,
    ) -> None:
        with self.database.session_factory() as session:
            account = session.get(Account, client_id)

            if account is None:
                raise ValueError("Account not found")

            session.delete(account)
            session.commit()
