import pytest
from sum_of_two import find_two_summands

testdata_unique_summands = [
    ([1, 3, 4, 10], 7, 1, 2),
    ([-10, -20, -3, -17], -20, 2, 3),
    ([10, 3, 10, 7], 10, 1, 3),
    ([10, 5, -3, -5], 5, 0, 3),
    ([10, -10_000, 1, 1], -9_990, 0, 1),
    ([-20, 0, 40, 0], 20, 0, 2),
]

testdata_repeating_summands = [
    ([5, 2, 2, 5], 10, 0, 3),
    ([-20, 0, 0, -3], 0, 1, 2),
    ([-250, -250, -250, -250, -500, -500], -1000, 4, 5),
]

testdata_extreme_summands = [
    ([500_000_000, 500_000_000], 1_000_000_000, 0, 1),
    ([-500_000_000, -500_000_000], -1_000_000_000, 0, 1),
    ([-1_000_000_000, 1_000_000_000], 0, 0, 1),
    ([1] * 9998 + [1_000_000_000, -1_000_000_000], 0, 9998, 9999),
]


@pytest.mark.parametrize(
    'arr,k,left_idx,right_idx',
    testdata_unique_summands + testdata_repeating_summands + testdata_extreme_summands,
)
def test_find_two_summands_unique_summands(
    arr: list[int], k: int, left_idx: int, right_idx: int
) -> None:
    answer = find_two_summands(arr, k)
    assert answer == (left_idx, right_idx)
