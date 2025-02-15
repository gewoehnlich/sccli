import asyncio
from aiohttp import web

class Server:
    def __init__(self) -> None:
        self.future = None

    async def run(self) -> tuple[str, str]:
        self.future = asyncio.get_event_loop().create_future()

        asyncio.create_task(self.start_server())
        print("Server started. Waiting for callback...")

        auth_code, state = await self.future
        return auth_code, state

    async def start_server(self) -> None:
        app = web.Application()
        app.router.add_get("/callback", self.callback_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8080)
        await site.start()
        print("Server is running at http://localhost:8080/callback")
        await self.future

    async def callback_handler(self, request):
        auth_code = request.query.get("code", None)
        state = request.query.get("state", None)

        if auth_code and state:
            print("Received code:", auth_code)
            print("Received state:", state)
            if not self.future.done():
                self.future.set_result((auth_code, state))
        else:
            print("No code parameter found.")

        return web.Response(
            text="Callback received. You may close this window."
        )

