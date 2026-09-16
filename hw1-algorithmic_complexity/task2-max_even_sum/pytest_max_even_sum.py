import pytest
from max_even_sum import max_even_sum

testdata_simple = [
    ([5, 7, 13, 2, 14], 36),
    ([5, 7, 5, 2, 14], 28),
    ([5, 7, 13, 5, 2, 14], 46),
    ([2, 4, 8], 14),
]

testdata_single_element_arrays = [([1], 0), ([9], 0), ([2], 2), ([4], 4)]


@pytest.mark.parametrize('array,max_even_arr_sum', testdata_simple)
def test_max_even_sum_simple_sums(array: list[int], max_even_arr_sum: int) -> None:
    answer = max_even_sum(array)
    assert answer == max_even_arr_sum


@pytest.mark.parametrize('array,max_even_arr_sum', testdata_single_element_arrays)
def test_max_even_sum_single_element_arrays(array: list[int], max_even_arr_sum: int) -> None:
    answer = max_even_sum(array)
    assert answer == max_even_arr_sum
