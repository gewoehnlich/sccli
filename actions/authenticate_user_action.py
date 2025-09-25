import asyncio
import webbrowser
from dependency_injector.wiring import Provide, inject

from core.dto import Dto
from main import DiContainer


class AuthenticateUserAction(
    Action
):
    @inject
    def run(
        self,
        auth_url: Url = Provide[DiContainer.url_generator.auth_url],
        generate_pkce: Task = Provide[DiContainer.tasks.generate_pkce],
        generate_state: Task = Provide[DiContainer.tasks.generate_state],
        request: Request = Provide[DiContainer.requests.authentication],
        server: Server = Provide[DiContainer.server],
    ) -> Dto:
        code_verifier, code_challenge: tuple[str, str] = generate_pkce()
        state: str = generate_state()

        webbrowser.open(
            url = auth_url,
        )

        auth_code, returned_state: tuple[str, str] = asyncio.run(
            main = server.run()
        )

        if state != returned_state:
            raise Exception("State mismatch!")

        # asdf
        request: Request = authentication_request(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            code_verifier,
            auth_code
        )

        response: Dto = request.send()
        
        return response

        # token_data: dict[str, Any] = JsonResource().from_dto(
        #     dto = response,
        # )
        #
        # with open(
        #     file = self.tokens_file,
        #     mode = "w",
        #     encoding = "utf-8",
        # ) as file:
        #     file.write(token_data)
        #
        # access_token: Any = response.access_token
        # if not isinstance(access_token, str):
        #     raise ValueError("access_token is not a string.")
        #
        # return access_token
