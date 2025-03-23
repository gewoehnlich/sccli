import os
import requests
import json
import asyncio
import aiohttp
from auth import Auth
from dotenv import load_dotenv
from requests.request import AsyncRequest
load_dotenv()

client_id = os.getenv("client_id")

async def main():
	async with AsyncRequest() as request_session:
		access_token = await Auth(request_session).get_access_token()
		print(access_token)

asyncio.run(main())

# track_id = 2010674763
#
# # Fetch the stream URL (follow redirects)
# stream_url = f"https://api.soundcloud.com/tracks/{track_id}/stream"
# headers = {"Authorization": f"OAuth {access_token}"}
# response = requests.get(stream_url, headers=headers, allow_redirects=True)
#
# # Get the final resolved URL (e.g., https://cf-media.sndcdn.com/...)
# final_url = response.url
# print("Final Stream URL:", final_url)
# os.system(f'vlc "{final_url}"')


# track_url = f"https://api.soundcloud.com/tracks/{TRACK_ID}"
# headers = {
#     "accept": "application/json; charset=utf-8",
#     "Authorization": f"OAuth {ACCESS_TOKEN}"
# }

# response = requests.get(track_url, headers=headers)
# if response.status_code == 200:
#     track_data = response.json()
#     print("Track Data:", track_data)  # Debugging

#     # 2️⃣ Get Stream URL
#     stream_url = f"https://api.soundcloud.com/tracks/{TRACK_ID}/stream"
#     stream_response = requests.get(stream_url, headers=headers)
#
#     if stream_response.status_code == 200:
#         final_stream_url = stream_response.json().get("url")  # Extract actual stream URL
#         print("Stream URL:", final_stream_url)  # Debugging
#
#         # 3️⃣ Play the track in VLC
#         if final_stream_url:
#             os.system(f'vlc "{final_stream_url}"')
#         else:
#             print("No valid stream URL found.")
#     else:
#         print("Error fetching stream URL:", stream_response.status_code, stream_response.text)
# else:
#     print("Error fetching track data:", response.status_code, response.text)
#
# headers = {
#     "accept": "application/json",
#     "charset": "utf-8",
#     "Authorization": f"Bearer {access_token}",
# }
#
# params = {
#     "limit": 2,
#     "access": ["playable"],
#     "linked_partitioning": True,
# }
#
# response = requests.get(
#     "https://api.soundcloud.com/me/likes/tracks",
#     headers=headers,
#     params=params
# )
#
# print(json.dumps(response.json(), indent=4, ensure_ascii=False))
#
# stream_url = response.json()["collection"][1]["stream_url"]
# full_url = f"{stream_url}?client_id={client_id}"
# os.system(f'vlc "{full_url}"')

# headers = {
#     "accept": "application/json",
#     "charset": "utf-8",
#     "Authorization": f"OAuth {access_token}",
# }
#
# response = requests.get(
#     song,
#     headers=headers
# )

# print(response.json())
# os.system(f"vlc \"{song}?client_id={client_id}\"")
