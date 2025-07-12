import typer
from src.core.auth import Auth

def main() -> None:
    test()

def test():
    auth = Auth()
    access_token = auth.get_access_token()
    print(access_token)

if __name__ == "__main__":
    typer.run(main)
