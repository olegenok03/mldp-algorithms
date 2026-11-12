import itertools
import math
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import pytest
from permutations import get_permutations, get_permutations_inplace

# Набор тестовых массивов (включая примеры из LeetCode 46 и краевые случаи)
test_arrays = [
    [],
    [1],
    [0, 1],
    [1, 2, 3],
    [-1, 0, 1],
    [4, 2, 7, 1],
]


# =====================================================================
# Тесты для Варианта 1: get_permutations (с булевой маской is_used)
# =====================================================================

def test_get_permutations_empty() -> None:
    assert get_permutations([]) == [[]]


def test_get_permutations_single() -> None:
    assert get_permutations([1]) == [[1]]


def test_get_permutations_two_elements() -> None:
    result = get_permutations([0, 1])
    expected = [[0, 1], [1, 0]]
    assert sorted(result) == sorted(expected)


def test_get_permutations_three_elements_leetcode_example() -> None:
    nums = [1, 2, 3]
    result = get_permutations(nums)
    expected = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert len(result) == 6
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize('arr', test_arrays)
def test_get_permutations_against_itertools(arr: list[int]) -> None:
    result = get_permutations(arr)
    expected = [list(p) for p in itertools.permutations(arr)]

    # 1. Количество перестановок равно N!
    assert len(result) == math.factorial(len(arr))

    # 2. Все перестановки уникальны
    unique_tuples = set(tuple(p) for p in result)
    assert len(unique_tuples) == len(result)

    # 3. Полное совпадение множества перестановок с эталоном itertools
    assert sorted(result) == sorted(expected)


def test_get_permutations_tracer_output(capsys: pytest.CaptureFixture[str]) -> None:
    get_permutations([1, 2])
    captured = capsys.readouterr()

    # Проверяем наличие вызовов функций и правильных отступов
    assert '"get_permutations" call with args ([1, 2],) and kwargs {}.' in captured.out
    assert '    "backtrack" call with args () and kwargs {}.' in captured.out
    assert '"get_permutations" terminated. Returned value: ' in captured.out


# =====================================================================
# Тесты для Варианта 2: get_permutations_inplace (In-Place Swapping)
# =====================================================================

def test_get_permutations_inplace_empty() -> None:
    assert get_permutations_inplace([]) == [[]]


def test_get_permutations_inplace_single() -> None:
    assert get_permutations_inplace([1]) == [[1]]


def test_get_permutations_inplace_two_elements() -> None:
    result = get_permutations_inplace([0, 1])
    expected = [[0, 1], [1, 0]]
    assert sorted(result) == sorted(expected)


def test_get_permutations_inplace_three_elements_leetcode_example() -> None:
    nums = [1, 2, 3]
    result = get_permutations_inplace(nums)
    expected = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert len(result) == 6
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize('arr', test_arrays)
def test_get_permutations_inplace_against_itertools(arr: list[int]) -> None:
    result = get_permutations_inplace(arr)
    expected = [list(p) for p in itertools.permutations(arr)]

    # 1. Количество перестановок равно N!
    assert len(result) == math.factorial(len(arr))

    # 2. Все перестановки уникальны
    unique_tuples = set(tuple(p) for p in result)
    assert len(unique_tuples) == len(result)

    # 3. Полное совпадение множества перестановок с эталоном itertools
    assert sorted(result) == sorted(expected)


def test_get_permutations_inplace_preserves_original_array() -> None:
    # Критическая проверка: массив не должен быть испорчен после работы
    original = [3, 2, 1, 5]
    input_copy = original.copy()

    _ = get_permutations_inplace(input_copy)

    # Входной массив обязан остаться в первозданном виде
    assert input_copy == original


def test_get_permutations_inplace_tracer_output(capsys: pytest.CaptureFixture[str]) -> None:
    get_permutations_inplace([1, 2])
    captured = capsys.readouterr()

    # Проверяем трассировку с отображением параметра first
    assert '"get_permutations_inplace" call with args ([1, 2],) and kwargs {}.' in captured.out
    assert '    "backtrack" call with args () and kwargs {}.' in captured.out
    assert '        "backtrack" call with args (1,) and kwargs {}.' in captured.out
    assert '"get_permutations_inplace" terminated. Returned value: ' in captured.out


# =====================================================================
# Сравнительный тест обоих вариантов
# =====================================================================

@pytest.mark.parametrize('arr', test_arrays)
def test_both_variants_yield_identical_sets(arr: list[int]) -> None:
    res1 = get_permutations(arr)
    res2 = get_permutations_inplace(arr)

    assert sorted(res1) == sorted(res2)
