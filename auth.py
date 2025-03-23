import os
import base64
import hashlib
import requests
import time
from dotenv import load_dotenv
import json
import asyncio
import webbrowser
from server import Server

class Auth:
    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")
        self.redirect_uri = "http://localhost:8080/callback"

    def get_access_token(self) -> None:
        access_token = self.load_token()
        if not access_token:
            access_token = self.authorize_user()

        return access_token

    def load_token(self) -> str | None:
        try:
            with open(".tokens", "r") as file:
                token_data = json.loads(file.read().strip())
                current_timestamp = int(time.time())
                expire_timestamp = (
                int(token_data["timestamp"]) + 
                int(token_data["expires_in"])
            )

            if current_timestamp > expire_timestamp - 100:
                if "refresh_token" not in token_data:
                    return None

                access_token = self.refresh_token(
                    token_data["refresh_token"]
                )

            else:
                access_token = token_data["access_token"]

            return access_token

        except (FileNotFoundError, KeyError):
            return None

    def refresh_token(self, refresh_token: str) -> str:
        refresh_url = "https://secure.soundcloud.com/oauth/token"
        headers = {
            "accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token
        }

        response = requests.post(
            refresh_url, 
            headers=headers, 
            data=data
        )

        print(refresh_url)
        print(headers)
        print(data)

        if not response:
            print("POST request failed: No response")
            return None

        try:
            token_data = response.json()
            token_data["timestamp"] = int(time.time()) 
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            return None

        with open(".tokens", "w") as file:
            file.write(json.dumps(token_data, indent=4))

        return token_data.get("access_token")

    def authorize_user(self) -> str:
        code_verifier, code_challenge = self.generate_pkce()
        state = self.generate_state()

        auth_url = (
            "https://secure.soundcloud.com/authorize"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            "&response_type=code"
            f"&code_challenge={code_challenge}"
            "&code_challenge_method=S256"
            f"&state={state}"
        )

        server = Server()
        webbrowser.open(auth_url)
        auth_code, returned_state = asyncio.run(server.run())
        if state != returned_state:
            raise Exception("State mismatch!")

        token_url = "https://secure.soundcloud.com/oauth/token"
        headers = {
            "accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
            "code": auth_code
        }

        response = requests.post(
            token_url, 
            headers=headers, 
            data=data
        )

        token_data = response.json()
        token_data["timestamp"] = int(time.time()) 

        with open(".tokens", "w") as file:
            file.write(json.dumps(token_data, indent=4))

        return token_data.get("access_token")

    def generate_pkce(self) -> tuple[str, str]:
        code_verifier = base64.urlsafe_b64encode(
            os.urandom(40)).decode("utf-8").rstrip("=")
        code_challenge = hashlib.sha256(
            code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(
            code_challenge).decode("utf-8").rstrip("=")

        return code_verifier, code_challenge

    def generate_state(self) -> str:
        state = base64.urlsafe_b64encode(
            os.urandom(16)).decode().rstrip("=")

        return state
