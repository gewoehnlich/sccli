from src.core.auth import Auth

def token() -> str:
    return Auth().get_access_token()
