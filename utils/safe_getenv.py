from os import getenv

def safe_getenv(key: str) -> str:
    value = getenv(key)
    if not value:
        raise ValueError(f"{key} is not set in .env file.")

    return value
