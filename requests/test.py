from request import AsyncRequest
import aiohttp
import asyncio

async def test_get():
    request = AsyncRequest()
    # print(request.session)
    # url = "https://postman-echo.com"
    url = "https://httpbin.org/get"
    headers = dict()
    # headers["x-forwarded-proto"] = "https"
    # headers["host"] = "postman-echo.com"
    # headers["accept"] = "*/*"
    # headers["accept-encoding"] = "gzip, deflate"
    # headers["cache-control"] = "no-cache"
    # headers["postman-token"] = "5c27cd7d-6b16-4e5a-a0ef-191c9a3a275f"
    # headers["user-agent"] = "PostmanRuntime/7.6.1"
    # headers["x-forwarded-port"] = "443"
    #
    params = dict()
    # params["foo1"] = "bar1"
    # params["foo2"] = "bar2"
    # params

    result = await request.get(url, headers, params)
    print(result)

# async def main():
#     await asyncio.sleep(1)
#     print("hello")

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())

asyncio.run(test_get())
# asyncio.run(main())
