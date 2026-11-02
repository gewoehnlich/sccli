from io import BytesIO

import requests
from PIL import Image as PILImage
from PIL.ImageFile import ImageFile
from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget
from textual_image.widget import Image as BaseImage

from loguru import logger

from actions.fetch_image_action import FetchImageAction


class Image(Widget):
    DEFAULT_IMAGE: str = "dist/image.jpg"

    image: Reactive[ImageFile | None] = reactive(None)

    def __init__(
        self,
        fetch_image_action: FetchImageAction,
    ) -> None:
        self.fetch_image_action = fetch_image_action

        super().__init__()

    def compose(self) -> ComposeResult:
        pil_image: ImageFile = PILImage.open(self.DEFAULT_IMAGE)

        yield BaseImage(pil_image)

    def on_mount(self) -> None:
        image = self.query_one(BaseImage)
        image.styles.width = "100%"
        image.styles.height = "100%"

    def watch_image(self, image: ImageFile | None) -> None:
        if image is not None:
            self.query_one(BaseImage).image = image

    def show_default(self) -> None:
        self.image = PILImage.open(self.DEFAULT_IMAGE)

    def load_artwork(self, url: str | None) -> None:
        image: ImageFile | None = None

        if url:
            try:
                proxy_endpoint = "http://172.17.0.1:52048"
                response = requests.get(url, timeout=5, proxies={"http": proxy_endpoint, "https": proxy_endpoint})

                image = PILImage.open(BytesIO(response.content))
                image.load()
            except (requests.RequestException, OSError):
                image = None

        if image is None:
            self.show_default()
        else:
            self.image = image
