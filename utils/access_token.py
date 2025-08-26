from core.auth import Auth

def access_token() -> str:
    return Auth().get_access_token()
