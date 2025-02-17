import os
import requests
import json
from auth import Auth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("client_id")

access_token = Auth().get_access_token()
headers = {
    "accept": "application/json",
    "charset": "utf-8",
    "Authorization": f"Bearer {access_token}",
}

params = {
    "limit": 2,
    "access": ["playable"],
    "linked_partitioning": True,
}

response = requests.get(
    "https://api.soundcloud.com/me/likes/tracks",
    headers=headers,
    params=params
)

# print(json.dumps(response.json(), indent=4, ensure_ascii=False))

song = response.json()["collection"][1]["stream_url"]
print(song)
print(client_id)
os.system(f"vlc \"{song}?client_id={client_id}\"")
