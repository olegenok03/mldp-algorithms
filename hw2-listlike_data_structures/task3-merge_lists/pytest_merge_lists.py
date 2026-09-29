import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from collections.abc import Callable

import pytest
from merge_lists import merge_sorted_lists_v1, merge_sorted_lists_v2
from stack_vs_queue import UDL, ListNode

testdata_unique_numbers = [
    ([-1, 0, 3, 5, 9, 10, 11, 12], [-2, 4, 6, 7, 8]),
    ([1024], [-1024]),
    ([1000], [0, 500, 1500, 2000, 2500]),
]

testdata_unique_non_overlapping_intervals = [
    (list(range(-1200, 210, 10)), list(range(210, 3210, 10))),
    ([1000], list(range(1001, 3001, 1))),
    (list(range(-1_000_000, 50, 30)), [50]),
]

testdata_repetitions = [
    ([1] * 100 + [3] * 200, [0] * 100 + [1] * 5 + [2] * 5 + [4] * 100),
    ([0] * 1000, [0]),
    (
        [-5] * 300 + [-4] * 300 + [-3] * 300 + [-2] * 300 + [-1] * 300,
        [-5] * 300 + [-4] * 300 + [-3] * 300 + [-2] * 300 + [-1] * 300,
    ),
]

testdata_empty = [
    ([], []),
    (list(range(-1_000_000, 50, 30)), []),
    ([], list(range(1001, 3001, 1))),
]


@pytest.mark.parametrize('merge_func', [merge_sorted_lists_v1, merge_sorted_lists_v2])
@pytest.mark.parametrize('arr1,arr2', testdata_unique_numbers)
def test_merge_func_unique_numbers(
    merge_func: Callable[[ListNode | None, ListNode | None], ListNode | None],
    arr1: list[int],
    arr2: list[int],
) -> None:
    sorted_arrs_concatenation = sorted(arr1 + arr2)

    merged_head = merge_func(UDL(arr1)._head, UDL(arr2)._head)
    merged_list = UDL.from_head_list_node(merged_head)

    assert sorted_arrs_concatenation == list(map(int, repr(merged_list).split()))


@pytest.mark.parametrize('merge_func', [merge_sorted_lists_v1, merge_sorted_lists_v2])
@pytest.mark.parametrize('arr1,arr2', testdata_unique_non_overlapping_intervals)
def test_merge_func_unique_non_overlapping_intervals(
    merge_func: Callable[[ListNode | None, ListNode | None], ListNode | None],
    arr1: list[int],
    arr2: list[int],
) -> None:
    sorted_arrs_concatenation = sorted(arr1 + arr2)

    merged_head = merge_func(UDL(arr1)._head, UDL(arr2)._head)
    merged_list = UDL.from_head_list_node(merged_head)

    assert sorted_arrs_concatenation == list(map(int, repr(merged_list).split()))


@pytest.mark.parametrize('merge_func', [merge_sorted_lists_v1, merge_sorted_lists_v2])
@pytest.mark.parametrize('arr1,arr2', testdata_repetitions)
def test_merge_func_repetitions(
    merge_func: Callable[[ListNode | None, ListNode | None], ListNode | None],
    arr1: list[int],
    arr2: list[int],
) -> None:
    sorted_arrs_concatenation = sorted(arr1 + arr2)

    merged_head = merge_func(UDL(arr1)._head, UDL(arr2)._head)
    merged_list = UDL.from_head_list_node(merged_head)

    assert sorted_arrs_concatenation == list(map(int, repr(merged_list).split()))


@pytest.mark.parametrize('merge_func', [merge_sorted_lists_v1, merge_sorted_lists_v2])
@pytest.mark.parametrize('arr1,arr2', testdata_empty)
def test_merge_func_empty(
    merge_func: Callable[[ListNode | None, ListNode | None], ListNode | None],
    arr1: list[int],
    arr2: list[int],
) -> None:
    sorted_arrs_concatenation = sorted(arr1 + arr2)

    merged_head = merge_func(UDL(arr1)._head, UDL(arr2)._head)
    merged_list = UDL.from_head_list_node(merged_head)

    assert sorted_arrs_concatenation == list(map(int, repr(merged_list).split()))
