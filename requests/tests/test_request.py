import os
import sys
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from request import AsyncRequest

request = AsyncRequest()


async def get_handler(request):
    return web.json_response({"method": "GET", "params": dict(request.query)})

async def post_handler(request):
    data = await request.post() if request.content_type == "application/x-www-form-urlencoded" else await request.json()
    return web.json_response({
        "method": "POST",
        "data": dict(data) if isinstance(data, web.MultiDict) else data,
        "content_type": request.content_type
    })

async def error_handler(request):
    return web.json_response({"error": "Not found"}, status=404)

@pytest.fixture
async def test_client(aiohttp_client):
    app = web.Application()
    app.router.add_get("/test-get", get_handler)
    app.router.add_post("/test-post", post_handler)
    app.router.add_get("/test-error", error_handler)
    client = TestClient(app)
    await client.start_server()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_get_success(test_client):
    async with test_client.get("/test-get") as response:
        assert response.status == 200

    async with AsyncRequest() as request:
        result = await request.get(
            test_client.make_url("/test-get").human_repr(),
            headers={"X-Test": "header"},
            params={"foo": "bar"}
        )
    
    assert result == {
        "method": "GET",
        "params": {"foo": "bar"}
    }

@pytest.mark.asyncio
async def test_get_error(test_client):
    async with AsyncRequest() as request:
        result = await request.get("/test-error")
    
    assert result is None

@pytest.mark.asyncio
async def test_post_form_data(test_client):
    async with AsyncRequest() as request:
        result = await request.post(
            "/test-post",
            headers={"X-Auth": "token"},
            data={"key": "value", "number": 42}
        )
    
    assert result == {
        "method": "POST",
        "data": {"key": "value", "number": "42"},  # Form data becomes strings
        "content_type": "application/x-www-form-urlencoded"
    }

@pytest.mark.asyncio
async def test_post_json(test_client):
    async with AsyncRequest() as request:
        result = await request.post(
            "/test-post",
            headers={"Content-Type": "application/json"},
            json={"nested": {"key": "value"}, "numbers": [1, 2, 3]}
        )
    
    assert result == {
        "method": "POST",
        "data": {"nested": {"key": "value"}, "numbers": [1, 2, 3]},
        "content_type": "application/json"
    }

@pytest.mark.asyncio
async def test_post_error():
    async with AsyncRequest() as request:
        result = await request.post("http://invalid-url")
    
    assert result is None
