import pytest

from core.config import Config


def test_config_file_is_not_present():
    with pytest.raises(FileNotFoundError):
        config = Config()
        config.CONFIG_PATH = 'asdfasdf.txt'
        config.load()
