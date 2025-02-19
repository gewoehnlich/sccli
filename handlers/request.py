import aiohttp
from typing import Optional, Any, Dict

# check for the right headers in post() data and json?
# Content-Type: application/x-www-form-urlencoded for data
# Content-Type: application/json for json

class AsyncRequest:
	def __init__(self):
		self.session = None

	async def __aenter__(self):
		self.session = aiohttp.ClientSession()
		return self

	async def __aexit__(self, exc_type, exc, tb):
		await self.session.close()

	async def get(
		self,
		url: str, 
		headers: Optional[Dict[str, str]] = None, 
		params: Optional[Dict[str, Any]] = None
	) -> Any:

		headers = headers or {}
		params = params or {}
		
		try:
			async with self.session.get(
				url, 
				headers=headers, 
				params=params
			) as response:
				response.raise_for_status()
				return await response.json()

		except (
			aiohttp.ClientError,
			aiohttp.http_exceptions.HttpProcessingError
		) as e:
			print(f"GET request failed: {e}")
			return None

	async def post(
		self,
		url: str, 
		headers: Optional[Dict[str, str]] = None, 
		data: Optional[Dict[str, Any]] = None, 
		json: Optional[Dict[str, Any]] = None
	) -> Any:

		headers = headers or {}
		
		print(url)
		print(headers)
		print(data)
		print(json)
		
		try:
			async with self.session.post(
				url, 
				headers=headers, 
				data=data, 
				json=json
			) as response:
				response.raise_for_status()
				return await response.json()

		except (
			aiohttp.ClientError,
			aiohttp.http_exceptions.HttpProcessingError
		) as e:
			print(f"POST request failed: {e}")
			return None

