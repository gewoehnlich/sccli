from typing import Annotated

from pydantic import StringConstraints

from config.base_config_model import BaseConfigModel

type SoundcloudCredentialsString = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=32,
        max_length=32,
        ascii_only=True,
    ),
]


class SoundcloudConfig(BaseConfigModel):
    client_id: SoundcloudCredentialsString
    client_secret: SoundcloudCredentialsString
