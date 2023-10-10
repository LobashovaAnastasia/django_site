import pytest
import logging


logger = logging.getLogger(__name__)


def is_even(num):
    try:
        if num % 2 == 0:
            return True
        if num % 2 == 1:
            return False
    except Exception:
        return "Invalid object passed."


@pytest.mark.parametrize(
    "number, expected",
    [
        (17, False),
        (18, True),
        (50, True),
        (100, True),
        (101, False),
    ]
)
def test_is_even(number, expected):
    result = is_even(number)

    logger.debug(f"Result: {result}")

    assert result is expected


@pytest.mark.parametrize(
    "object, expected",
    [
        ("12345", "Invalid object passed."),
        ([1, 2, 3, 4, 5], "Invalid object passed.")
    ]
)
def test_is_even_err(object, expected):
    result = is_even(object)

    logger.debug(f"Result: {result}")

    assert result is expected
