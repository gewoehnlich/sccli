import os
import base64
import hashlib
import requests
import threading
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

    def main(self) -> None:
        access_token = self.load_token()
        if not access_token:
            access_token = self.authorize_user()

        return access_token

    def load_token(self) -> str | None:
        try:
            with open(".tokens", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

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

        response = requests.post(token_url, headers=headers, data=data)
        token_data = response.json()
        print(token_data)

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

    def run_server_in_thread(self):
        asyncio.run(Server().start_server())

    def run_server(self):
        server_thread = threading.Thread(
            target=self.run_server_in_thread, 
            daemon=True
        )
        server_thread.start()

    def get_auth_code(self, auth_url: str) -> str:
        print(f"Open this URL in your browser:\n\n{auth_url}\n")
        print("After logging in, you'll be redirected to a blank page.")
        print("Copy the 'code' parameter from the URL and paste it below.\n")

        auth_code = input("Paste the code here: ").strip()
        return auth_code

