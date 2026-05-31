from io import BytesIO

from PIL.ImageFile import ImageFile
import requests
from PIL import Image as PILImage

from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget
from textual_image.widget import Image as BaseImage

class Image(Widget):
    image: Reactive[ImageFile | None] = reactive(None)

    DEFAULT_IMAGE: str = 'dist/image.jpg'

    def compose(self) -> ComposeResult:
        pil_image: ImageFile = PILImage.open(self.DEFAULT_IMAGE)

        self.base_image = BaseImage(pil_image)
        yield self.base_image

    def on_mount(self) -> None:
        self.base_image.styles.width = "100%"
        self.base_image.styles.height = "100%"

    def update(
        self,
        image: ImageFile,
    ) -> None:
        self.image = image

    def update_from_link(
        self,
        link: str,
    ) -> None:
        response = requests.get(link, timeout=5)

        pil_image: ImageFile = PILImage.open(
            BytesIO(response.content),
        )

        self.update(image=pil_image)

    def update_from_local(
        self,
        filename: str,
    ) -> None:
        pil_image: ImageFile = PILImage.open(filename)

        self.update(image=pil_image)
