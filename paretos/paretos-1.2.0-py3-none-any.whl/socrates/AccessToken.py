from datetime import datetime, timedelta, timezone

TOKEN_BUFFER_SECONDS = 60


class AccessToken:
    def __init__(self, access_token: str, expires: datetime):
        self.__token = access_token
        self.__expires = expires

    def get_access_token(self) -> str:
        return self.__token

    def is_token_expired(self) -> bool:
        buffer = timedelta(seconds=TOKEN_BUFFER_SECONDS)
        return datetime.now(tz=timezone.utc) + buffer > self.__expires
