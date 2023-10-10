import logging

import pytest
import itertools

"""
Conditions:
- age is ALWAYS integer
- age should be in range between 18 and 100 including
- NOTE: age may pass as negative integer!
"""

_RANGE = set(range(18, 101))

logger = logging.getLogger(__name__)


def check_age_is_correct(age: int) -> bool:
    if age in _RANGE:
        return True

    return False


def divide(arg1: int, arg2: int) -> float:
    return arg1 / arg2


@pytest.mark.parametrize(
    "age, expected",  # parameters names
    [
        (17, False),
        (18, True),
        (50, True),
        (100, True),
        (101, False),
    ]   # list of tests_2 values: each value is 2-tuple because we have 2 params
)
def test_age_is_correct(
    # don't forget to pass arguments names defined in *parametrize*
    # to test arguments!
    age,
    expected
):
    # act
    result = check_age_is_correct(age)

    logger.debug(f"Result: {result}")

    # assert
    assert result is expected


@pytest.mark.skip
def test_divide__negative():
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide(100, 1)

    exc_data = exc_info.value.args

    assert True


"""
itertools.product can be used to create combinations
for the tests_2 parameters.
Example:
"""
x = [17, 18, 50, 100, 101]
y = ['Alex', 'Kate', 'John', 'Ann']
print(list(itertools.product(x, y)))

"""
itertools.chain is used to chain the generators/iterators 
as one sequential iterator:
"""

it1 = iter([1, 2, 3])
it2 = iter([4, 5, 6])
print(list(itertools.chain(it1, it2)))

"""
itertools.chain.from_iterable is used to make
"flat" collection from the collection with nested collections
"""
x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
assert list(itertools.chain.from_iterable(x)) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

# NOTE: it covers only the first nesting level!
y = [[1, 2, 3], [4, 5, 6, [7, 8, 9]]]
assert list(itertools.chain.from_iterable(y)) == [1, 2, 3, 4, 5, 6, [7, 8, 9]]


