import os
import random
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import pytest
from iterative_quick_and_merge import (
    merge_sort_iterative,
    quick_sort_iterative,
)

# =====================================================================
# Набор тестовых данных для всесторонней проверки сортировок
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
    [2, 1, 4, 3, 6, 5, 8, 7],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]


# =====================================================================
# 1. Тесты корректности Merge Sort (итеративный)
# =====================================================================

@pytest.mark.parametrize('arr', test_cases)
def test_merge_sort_iterative_correctness(arr: list[int]) -> None:
    original = arr.copy()
    sorted_arr = merge_sort_iterative(arr)
    assert sorted_arr == sorted(arr)
    assert arr == original, 'Исходный массив не должен изменяться (immutability)'


def test_merge_sort_iterative_large_random() -> None:
    random.seed(42)
    data = [random.randint(-10000, 10000) for _ in range(3000)]
    assert merge_sort_iterative(data) == sorted(data)


def test_merge_sort_iterative_stability() -> None:
    # Проверка устойчивости: элементы с одинаковым ключом должны сохранить взаимный порядок
    data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (2, 'e'), (1, 'f')]
    sorted_data = merge_sort_iterative(data)
    expected = [(1, 'b'), (1, 'd'), (1, 'f'), (2, 'a'), (2, 'c'), (2, 'e')]
    assert sorted_data == expected


# =====================================================================
# 2. Тесты корректности Quick Sort (итеративный)
# =====================================================================

@pytest.mark.parametrize('arr', test_cases)
def test_quick_sort_iterative_correctness(arr: list[int]) -> None:
    original = arr.copy()
    sorted_arr = quick_sort_iterative(arr)
    assert sorted_arr == sorted(arr)
    assert arr == original, 'Исходный массив не должен изменяться (immutability)'


def test_quick_sort_iterative_large_random() -> None:
    random.seed(42)
    data = [random.randint(-10000, 10000) for _ in range(3000)]
    assert quick_sort_iterative(data) == sorted(data)


def test_quick_sort_iterative_sorted_and_reversed() -> None:
    # В итеративной версии глубина не ограничена лимитом системного стека Python (1000),
    # так как стек хранится в куче (heap-allocated list)
    sorted_data = list(range(1500))
    reversed_data = list(range(1500, 0, -1))

    assert quick_sort_iterative(sorted_data) == sorted_data
    assert quick_sort_iterative(reversed_data) == list(range(1, 1501))


def test_quick_sort_iterative_identical_elements() -> None:
    data = [42] * 1500
    assert quick_sort_iterative(data) == data


# =====================================================================
# 3. Специальные и нетривиальные случаи
# =====================================================================

@pytest.mark.parametrize('n', [3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65])
def test_powers_of_two_boundaries(n: int) -> None:
    # Критично для Bottom-Up слияния: проверка границ вокруг степеней двойки
    data = list(range(n, 0, -1))
    expected = list(range(1, n + 1))
    assert merge_sort_iterative(data) == expected
    assert quick_sort_iterative(data) == expected


@pytest.mark.parametrize(
    'zigzag',
    [
        [1, 100, 2, 99, 3, 98, 4, 97, 5, 96],
        [10, 1, 9, 2, 8, 3, 7, 4, 6, 5],
        [5, 1, 5, 2, 5, 3, 5, 4],
    ],
)
def test_zigzag_sawtooth_arrays(zigzag: list[int]) -> None:
    # Пилообразные (зигзагообразные) массивы с частой сменой локальных экстремумов
    expected = sorted(zigzag)
    assert merge_sort_iterative(zigzag) == expected
    assert quick_sort_iterative(zigzag) == expected


