import os
import requests
import json
from auth import Auth
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("client_id")
auth = Auth()
print(auth.get_access_token())
