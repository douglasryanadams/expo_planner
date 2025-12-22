import sys
from loguru import logger
import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_loguru():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> <level>{level: <8}</level> - <level>{message}</level>",
        level="DEBUG",
        colorize=True,
    )
    yield


@pytest.fixture
def caplog_loguru(capfd):
    yield
    captured = capfd.readouterr()
    return captured
