import pytest
import logging
import re


logger = logging.getLogger(__name__)


def func(obj):
    regex_pattern = r"^[a-zA-Z0-9]+$"
    if re.match(regex_pattern, obj) is not None:
        return True
    else:
        return False


@pytest.mark.parametrize(
    "object, expected",
    [
        ("Hello!", False),
        ("Python", True),
        ("50", True),
        ("A100", True),
        ("Привет", False),
        ("Hello world", False),
    ]
)
def test_str(object, expected):
    result = func(object)

    logger.debug(f"Result: {result}")

    assert result is expected
