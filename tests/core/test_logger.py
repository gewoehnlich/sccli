import re
from collections.abc import Iterator
from pathlib import Path

import pytest
from loguru import logger

from enums.logger_level import LoggerLevelEnum
from core.logger import Logger


@pytest.fixture(autouse=True)
def reset_loguru() -> Iterator[None]:
    yield
    logger.remove()  # no handler leaks into other tests


@pytest.fixture
def log_dir(tmp_path: Path) -> Path:
    return tmp_path / "logs"


@pytest.fixture
def level() -> LoggerLevelEnum:
    return LoggerLevelEnum.INFO


def read_log(directory: Path) -> str:
    files = list(directory.glob("*.log"))
    assert len(files) == 1
    return files[0].read_text(encoding="utf-8")


def test_creates_directory_and_dated_file(log_dir: Path, level: LoggerLevelEnum) -> None:
    log = Logger(directory=log_dir, level=level)

    text = "hello"
    log.info(text)

    log.close()

    files = list(log_dir.glob("*.log"))

    assert len(files) == 1
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}\.log", files[0].name)
    assert text in files[0].read_text(encoding="utf-8")


def test_default_level_hides_lower_level_logs(log_dir: Path) -> None:
    level = LoggerLevelEnum.INFO

    log = Logger(directory=log_dir, level=level)

    debug_text = "debug_text"
    log.debug(debug_text)

    info_text = "info_text"
    log.info(info_text)

    log.close()

    text = read_log(log_dir)

    assert debug_text not in text
    assert info_text in text


@pytest.mark.parametrize(
    ("method", "level"),
    [
        ("trace", LoggerLevelEnum.TRACE),
        ("debug", LoggerLevelEnum.DEBUG),
        ("info", LoggerLevelEnum.INFO),
        ("success", LoggerLevelEnum.SUCCESS),
        ("warning", LoggerLevelEnum.WARNING),
        ("error", LoggerLevelEnum.ERROR),
        ("critical", LoggerLevelEnum.CRITICAL),
    ],
)
def test_each_method_logs_at_its_level(log_dir: Path, method: str, level: LoggerLevelEnum) -> None:
    log = Logger(directory=log_dir, level=level)
    getattr(log, method)("msg")
    log.close()

    assert re.search(rf"\| {level.value}\s+\|", read_log(log_dir))


def test_records_caller_location_not_wrapper(log_dir: Path, level: LoggerLevelEnum) -> None:
    log = Logger(directory=log_dir, level=level)
    log.info("where")
    log.close()

    assert "test_records_caller_location_not_wrapper" in read_log(log_dir)


def test_exception_includes_traceback(log_dir: Path, level: LoggerLevelEnum) -> None:
    log = Logger(directory=log_dir, level=level)

    try:
        raise ValueError("boom")
    except ValueError:
        log.exception("failed")

    log.close()

    text = read_log(log_dir)
    assert "failed" in text
    assert "ValueError: boom" in text


def test_close_stops_writing(log_dir: Path, level: LoggerLevelEnum) -> None:
    log = Logger(directory=log_dir, level=level)

    before_text = "before_text"
    log.info(before_text)

    log.close()

    after_text = "after_text"
    log.info(after_text)

    text = read_log(log_dir)
    assert before_text in text
    assert after_text not in text
