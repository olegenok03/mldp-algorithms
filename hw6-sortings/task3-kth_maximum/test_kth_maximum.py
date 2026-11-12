import os
import random
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import pytest
from kth_maximum import kth_maximum


# =====================================================================
# 1. Примеры из условия учебного задания (LeetCode 215)
# =====================================================================

def test_kth_maximum_assignment_examples() -> None:
    # Пример 1: [3, 2, 1, 5, 6, 4], k = 2 -> 5 (1-й: 6, 2-й: 5)
    assert kth_maximum([3, 2, 1, 5, 6, 4], 2) == 5

    # Пример 2: [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4 -> 4
    # По убыванию: [6, 5, 5, 4, 3, 3, 2, 2, 1], 4-й элемент — 4
    assert kth_maximum([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


# =====================================================================
# 2. Тривиальные и базовые случаи
# =====================================================================

def test_single_element() -> None:
    assert kth_maximum([42], 1) == 42
    assert kth_maximum([-100], 1) == -100


@pytest.mark.parametrize(
    'arr,k,expected',
    [
        ([1, 2], 1, 2),  # 1-й максимум в [1, 2] -> 2
        ([1, 2], 2, 1),  # 2-й максимум в [1, 2] -> 1
        ([2, 1], 1, 2),  # 1-й максимум в [2, 1] -> 2
        ([2, 1], 2, 1),  # 2-й максимум в [2, 1] -> 1
    ],
)
def test_two_elements(arr: list[int], k: int, expected: int) -> None:
    assert kth_maximum(arr, k) == expected


# =====================================================================
# 3. Краевые случаи (границы диапазона k, знаки, дубликаты, иммутабельность)
# =====================================================================

@pytest.mark.parametrize(
    'arr',
    [
        [10, 5, 20, 3, 8],
        [-1, -10, -5, -2],
        [100],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
    ],
)
def test_extreme_k_boundaries(arr: list[int]) -> None:
    # k = 1 всегда должен возвращать максимальный элемент массива
    assert kth_maximum(arr, 1) == max(arr)

    # k = len(arr) всегда должен возвращать минимальный элемент массива
    assert kth_maximum(arr, len(arr)) == min(arr)


def test_negative_numbers_and_zeros() -> None:
    data = [-5, 0, -10, 15, -2, 0, 7]
    sorted_desc = sorted(data, reverse=True)  # [15, 7, 0, 0, -2, -5, -10]

    for k in range(1, len(data) + 1):
        assert kth_maximum(data, k) == sorted_desc[k - 1]


def test_all_elements_identical() -> None:
    data = [7] * 10
    for k in range(1, len(data) + 1):
        assert kth_maximum(data, k) == 7


def test_heavy_duplicates() -> None:
    data = [1, 2, 2, 3, 3, 3, 4]
    sorted_desc = sorted(data, reverse=True)  # [4, 3, 3, 3, 2, 2, 1]

    for k in range(1, len(data) + 1):
        assert kth_maximum(data, k) == sorted_desc[k - 1]


def test_original_array_is_not_mutated() -> None:
    original = [5, 2, 8, 1, 9, 3]
    clone = original.copy()

    _ = kth_maximum(original, 3)

    assert original == clone, 'Функция kth_maximum не должна мутировать исходный массив'


# =====================================================================
# 4. Худшие случаи (Worst-Case Scenarios для алгоритмов типа QuickSort)
# =====================================================================

def test_worst_case_strictly_sorted_ascending() -> None:
    # Отсортированный массив: при детерминированном pivot алгоритм деградирует в O(N^2),
    # но при случайном pivot должен отрабатывать стабильно и быстро
    data = list(range(1, 1001))
    assert kth_maximum(data, 1) == 1000
    assert kth_maximum(data, 500) == 501
    assert kth_maximum(data, 1000) == 1


def test_worst_case_strictly_sorted_descending() -> None:
    data = list(range(1000, 0, -1))
    assert kth_maximum(data, 1) == 1000
    assert kth_maximum(data, 250) == 751
    assert kth_maximum(data, 1000) == 1


def test_worst_case_all_identical_large() -> None:
    # Массив из одинаковых элементов: в схеме Ломуто все элементы переходят в одну ветку
    data = [42] * 1200
    assert kth_maximum(data, 1) == 42
    assert kth_maximum(data, 600) == 42
    assert kth_maximum(data, 1200) == 42


# =====================================================================
# 5. Стресс-тестирование на случайных данных
# =====================================================================

def test_all_k_on_random_array() -> None:
    # Полная проверка корректности для каждого k от 1 до N
    random.seed(12345)
    data = [random.randint(-1000, 1000) for _ in range(100)]
    expected_desc = sorted(data, reverse=True)

    for k in range(1, len(data) + 1):
        assert kth_maximum(data, k) == expected_desc[k - 1]


def test_large_random_array_stress() -> None:
    # Большой стресс-тест на массиве из 5000 элементов
    random.seed(54321)
    data = [random.randint(-100_000, 100_000) for _ in range(5000)]
    expected_desc = sorted(data, reverse=True)

    check_k_values = [1, 2, 10, 50, 500, 2500, 4990, 5000]
    for k in check_k_values:
        assert kth_maximum(data, k) == expected_desc[k - 1]

