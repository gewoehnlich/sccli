from dotenv import load_dotenv
from src.core.shell import shell

if __name__ == "__main__":
    # for .env file variables
    load_dotenv()

    # start shell session
    shell()
