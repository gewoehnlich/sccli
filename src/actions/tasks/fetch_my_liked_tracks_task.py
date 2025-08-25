from src.core.task import Task 

class FetchMyLikedTracksTask(Task):
    def run(self) -> bool:
        _COLLECTION = "collection"
        _NEXT_HREF  = "next_href"

        request: UsersLikedTracksRequest = UsersLikedTracksRequest()
        response: Response = send_request(request = request)

        result: dict[str, Any] = response.json()

        collection: dict[str, Any] = result[_COLLECTION]
        next_href: str | None = result[_NEXT_HREF]

        if collection:
            pprint(collection)

        if next_href:
            pprint(next_href)
