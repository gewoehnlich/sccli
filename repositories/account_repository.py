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


    def write(
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
