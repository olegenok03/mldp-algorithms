from itertools import permutations

import pytest
from push_pop_sequence import validate_push_pop_sequence

testdata_simple_true = [
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], True),
    ([1, 2, 3, 4, 5], [1, 2, 3, 5, 4], True),
    ([1, 2, 3, 4, 5], [1, 2, 4, 3, 5], True),
    ([1, 2, 3, 4, 5], [1, 2, 4, 5, 3], True),
    ([1, 2, 3, 4, 5], [1, 2, 5, 4, 3], True),
    ([1, 2, 3, 4, 5], [1, 3, 2, 4, 5], True),
    ([1, 2, 3, 4, 5], [1, 3, 2, 5, 4], True),
    ([1, 2, 3, 4, 5], [1, 3, 4, 2, 5], True),
    ([1, 2, 3, 4, 5], [1, 3, 4, 5, 2], True),
    ([1, 2, 3, 4, 5], [1, 3, 5, 4, 2], True),
    ([1, 2, 3, 4, 5], [1, 4, 3, 2, 5], True),
    ([1, 2, 3, 4, 5], [1, 4, 3, 5, 2], True),
    ([1, 2, 3, 4, 5], [1, 4, 5, 3, 2], True),
    ([1, 2, 3, 4, 5], [1, 5, 4, 3, 2], True),
    ([1, 2, 3, 4, 5], [2, 1, 3, 4, 5], True),
    ([1, 2, 3, 4, 5], [2, 1, 3, 5, 4], True),
    ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5], True),
    ([1, 2, 3, 4, 5], [2, 1, 4, 5, 3], True),
    ([1, 2, 3, 4, 5], [2, 1, 5, 4, 3], True),
    ([1, 2, 3, 4, 5], [2, 3, 1, 4, 5], True),
    ([1, 2, 3, 4, 5], [2, 3, 1, 5, 4], True),
    ([1, 2, 3, 4, 5], [2, 3, 4, 1, 5], True),
    ([1, 2, 3, 4, 5], [2, 3, 4, 5, 1], True),
    ([1, 2, 3, 4, 5], [2, 3, 5, 4, 1], True),
    ([1, 2, 3, 4, 5], [2, 4, 3, 1, 5], True),
    ([1, 2, 3, 4, 5], [2, 4, 3, 5, 1], True),
    ([1, 2, 3, 4, 5], [2, 4, 5, 3, 1], True),
    ([1, 2, 3, 4, 5], [2, 5, 4, 3, 1], True),
    ([1, 2, 3, 4, 5], [3, 2, 1, 4, 5], True),
    ([1, 2, 3, 4, 5], [3, 2, 1, 5, 4], True),
    ([1, 2, 3, 4, 5], [3, 2, 4, 1, 5], True),
    ([1, 2, 3, 4, 5], [3, 2, 4, 5, 1], True),
    ([1, 2, 3, 4, 5], [3, 2, 5, 4, 1], True),
    ([1, 2, 3, 4, 5], [3, 4, 2, 1, 5], True),
    ([1, 2, 3, 4, 5], [3, 4, 2, 5, 1], True),
    ([1, 2, 3, 4, 5], [3, 4, 5, 2, 1], True),
    ([1, 2, 3, 4, 5], [3, 5, 4, 2, 1], True),
    ([1, 2, 3, 4, 5], [4, 3, 2, 1, 5], True),
    ([1, 2, 3, 4, 5], [4, 3, 2, 5, 1], True),
    ([1, 2, 3, 4, 5], [4, 3, 5, 2, 1], True),
    ([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True),
    ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], True),
]

testdata_simple_false = [
    ([1, 2, 3, 4, 5], perm, False)
    for perm in map(list, permutations([1, 2, 3, 4, 5]))
    if perm not in (x[1] for x in testdata_simple_true)
]

testdata_single_element_arrays = [
    ([1], [1], True),
    ([9], [9], True),
    ([2], [2], True),
    ([4], [4], True),
]


@pytest.mark.parametrize('pushed,popped,is_valid', testdata_simple_true)
def test_validate_push_pop_sequence_simple_true_samples(
    pushed: list[int], popped: list[int], is_valid: bool
) -> None:
    answer = validate_push_pop_sequence(pushed, popped)
    assert answer == is_valid


@pytest.mark.parametrize('pushed,popped,is_valid', testdata_simple_false)
def test_validate_push_pop_sequence_simple_false_samples(
    pushed: list[int], popped: list[int], is_valid: bool
) -> None:
    answer = validate_push_pop_sequence(pushed, popped)
    assert answer == is_valid


@pytest.mark.parametrize('pushed,popped,is_valid', testdata_single_element_arrays)
def test_max_even_sum_single_element_arrays(
    pushed: list[int], popped: list[int], is_valid: bool
) -> None:
    answer = validate_push_pop_sequence(pushed, popped)
    assert answer == is_valid
