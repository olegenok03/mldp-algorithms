import os
import random
import sys
import time

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import pytest
from recursive_quick_and_merge import (
    benchmark,
    merge_sort_recursive,
    quick_sort_recursive,
)

# =====================================================================
# 1. Тесты декоратора benchmark
# =====================================================================


def test_benchmark_preserves_metadata() -> None:
    @benchmark
    def sample_func(x: int) -> int:
        """Docstring for sample_func."""
        return x * 2

    assert sample_func.__name__ == 'sample_func'
    assert sample_func.__doc__ == 'Docstring for sample_func.'


def test_benchmark_return_type_and_elapsed_time() -> None:
    @benchmark
    def sleepy_func(duration: float) -> str:
        time.sleep(duration)
        return 'done'

    res, elapsed = sleepy_func(0.02)
    assert res == 'done'
    assert isinstance(elapsed, float)
    assert elapsed >= 0.015


# =====================================================================
# 2. Набор тестовых данных для проверки корректности сортировки
# =====================================================================

test_cases = [
    [],
    [42],
    [1, 2],
    [2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
    [-5, 0, 5, -10, 100, -2],
    [7, 7, 7, 7, 7],
    [10, -1, 2, 8, 3, 7, 4, 6, 5],
]


@pytest.mark.parametrize('arr', test_cases)
def test_merge_sort_correctness(arr: list[int]) -> None:
    original = arr.copy()
    sorted_arr = merge_sort_recursive(arr)
    assert sorted_arr == sorted(arr)
    assert arr == original, 'Исходный массив не должен изменяться (immutability)'


@pytest.mark.parametrize('arr', test_cases)
def test_quick_sort_correctness(arr: list[int]) -> None:
    original = arr.copy()
    sorted_arr = quick_sort_recursive(arr)
    assert sorted_arr == sorted(arr)
    assert arr == original, 'Исходный массив не должен изменяться (immutability)'


def test_sorts_on_large_random_array() -> None:
    random.seed(42)
    data = [random.randint(-10000, 10000) for _ in range(2000)]
    expected = sorted(data)

    assert merge_sort_recursive(data) == expected
    assert quick_sort_recursive(data) == expected


def test_merge_sort_stability() -> None:
    # Проверка устойчивости: элементы с одинаковым ключом должны сохранить взаимный порядок
    data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (2, 'e')]
    sorted_data = merge_sort_recursive(data)
    expected = [(1, 'b'), (1, 'd'), (2, 'a'), (2, 'c'), (2, 'e')]
    assert sorted_data == expected


# =====================================================================
# 3. Дополнительные тесты согласно заданию:
#    «Придумать тесты, на которых время выполнения этих методов
#     будет прилично отличаться»
# =====================================================================


@pytest.fixture
def timed_merge_sort():
    return benchmark(merge_sort_recursive)


@pytest.fixture
def timed_quick_sort():
    return benchmark(quick_sort_recursive)


def test_benchmark_sorted_array_merge_substantially_faster(
    timed_merge_sort, timed_quick_sort
) -> None:
    """
    Тест 1: Уже отсортированный массив.
    - MergeSort: благодаря проверке arr_copy[mid] <= arr_copy[mid + 1] работает за O(N).
    - QuickSort (Lomuto с pivot на конце): деградирует до O(N^2) и совершает N рекурсивных вызовов.
    Ожидается колоссальное превосходство MergeSort.
    """
    n = 800
    sorted_data = list(range(n))

    res_merge, time_merge = timed_merge_sort(sorted_data)
    res_quick, time_quick = timed_quick_sort(sorted_data)

    assert res_merge == sorted_data
    assert res_quick == sorted_data
    # MergeSort на O(N) опережает O(N^2) QuickSort как минимум в 5-10 раз
    assert time_merge < time_quick
    assert time_quick / max(time_merge, 1e-9) > 3.0


def test_benchmark_reversed_array_merge_substantially_faster(
    timed_merge_sort, timed_quick_sort
) -> None:
    """
    Тест 2: Обратно отсортированный массив.
    - MergeSort: строго делит пополам, O(N log N).
    - QuickSort: наихудшее разбиение для Ломуто, O(N^2).
    """
    n = 800
    reversed_data = list(range(n, 0, -1))

    res_merge, time_merge = timed_merge_sort(reversed_data)
    res_quick, time_quick = timed_quick_sort(reversed_data)

    expected = list(range(1, n + 1))
    assert res_merge == expected
    assert res_quick == expected
    assert time_merge < time_quick
    assert time_quick / max(time_merge, 1e-9) > 2.0


def test_benchmark_identical_elements_merge_substantially_faster(
    timed_merge_sort, timed_quick_sort
) -> None:
    """
    Тест 3: Массив из одинаковых элементов.
    - MergeSort: проверка arr_copy[mid] <= arr_copy[mid + 1] делает работу за O(N).
    - QuickSort (Lomuto): при arr[j] <= pivot каждый элемент сдвигает указатель i,
      разбиение дает подмассив длины N-1, деградируя в O(N^2).
    """
    n = 800
    identical_data = [42] * n

    res_merge, time_merge = timed_merge_sort(identical_data)
    res_quick, time_quick = timed_quick_sort(identical_data)

    assert res_merge == identical_data
    assert res_quick == identical_data
    assert time_merge < time_quick
    assert time_quick / max(time_merge, 1e-9) > 3.0


def test_benchmark_random_array_quick_faster(
    timed_merge_sort, timed_quick_sort
) -> None:
    """
    Тест 4: Большой случайный массив.
    - QuickSort: в среднем O(N log N) с маленькой скрытой константой (in-place swap, кэш-локальность).
    - MergeSort: O(N log N), но имеет константу за счет копирования элементов в aux-буфер.
    На больших случайных данных QuickSort быстрее или сопоставим.
    """
    random.seed(123)
    data = [random.randint(0, 100_000) for _ in range(15_000)]

    res_merge, time_merge = timed_merge_sort(data)
    res_quick, time_quick = timed_quick_sort(data)

    expected = sorted(data)
    assert res_merge == expected
    assert res_quick == expected
    assert time_merge > 0 and time_quick > 0
