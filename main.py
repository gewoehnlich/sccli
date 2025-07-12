from src.utils.shell import shell
from src.core.auth import Auth
from dotenv import load_dotenv

if __name__ == "__main__":
    # start shell session
    load_dotenv()
    # shell()
    auth = Auth()
    access_token = auth.get_access_token()
    print(access_token)
