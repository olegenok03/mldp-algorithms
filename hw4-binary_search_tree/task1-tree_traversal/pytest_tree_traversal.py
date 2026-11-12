import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from binary_search_tree import BinarySearchTree

# Наборы данных: (keys, expected_preorder, expected_inorder, expected_postorder, expected_rev_pre, expected_rev_in, expected_rev_post)
testdata_basic = [
    # Один узел
    ([42], [42], [42], [42], [42], [42], [42]),
    # Два узла: корень и левый ребенок
    ([10, 5], [10, 5], [5, 10], [5, 10], [10, 5], [10, 5], [5, 10]),
    # Два узла: корень и правый ребенок
    ([10, 15], [10, 15], [10, 15], [15, 10], [10, 15], [15, 10], [15, 10]),
]

testdata_skewed = [
    # Вырожденное дерево (только левые дети)
    (
        [5, 4, 3, 2, 1],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
    ),
    # Вырожденное дерево (только правые дети)
    (
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [5, 4, 3, 2, 1],
    ),
    # Пилообразное (зигзаг) дерево
    (
        [5, 1, 4, 2, 3],
        [5, 1, 4, 2, 3],
        [1, 2, 3, 4, 5],
        [3, 2, 4, 1, 5],
        [5, 1, 4, 2, 3],
        [5, 4, 3, 2, 1],
        [3, 2, 4, 1, 5],
    ),
]

testdata_complex = [
    # Полное/сбалансированное бинарное дерево поиска
    (
        [4, 2, 1, 3, 6, 5, 7],
        [4, 2, 1, 3, 6, 5, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 3, 2, 5, 7, 6, 4],
        [4, 6, 7, 5, 2, 3, 1],
        [7, 6, 5, 4, 3, 2, 1],
        [7, 5, 6, 3, 1, 2, 4],
    ),
    # Классическое разветвленное дерево
    (
        [8, 3, 1, 6, 4, 7, 10, 14, 13],
        [8, 3, 1, 6, 4, 7, 10, 14, 13],
        [1, 3, 4, 6, 7, 8, 10, 13, 14],
        [1, 4, 7, 6, 3, 13, 14, 10, 8],
        [8, 10, 14, 13, 3, 6, 7, 4, 1],
        [14, 13, 10, 8, 7, 6, 4, 3, 1],
        [13, 14, 10, 7, 4, 6, 1, 3, 8],
    ),
    # Отрицательные числа и ноль
    (
        [0, -10, -20, -5, 10, 5, 20],
        [0, -10, -20, -5, 10, 5, 20],
        [-20, -10, -5, 0, 5, 10, 20],
        [-20, -5, -10, 5, 20, 10, 0],
        [0, 10, 20, 5, -10, -5, -20],
        [20, 10, 5, 0, -5, -10, -20],
        [20, 5, 10, -5, -20, -10, 0],
    ),
]

all_testdata = testdata_basic + testdata_skewed + testdata_complex


@pytest.mark.parametrize(
    'keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post',
    all_testdata,
)
def test_preorder_traversal(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_preorder() == expected_pre


@pytest.mark.parametrize(
    'keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post',
    all_testdata,
)
def test_reverse_preorder_traversal(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_reverse_preorder() == expected_rev_pre


@pytest.mark.parametrize(
    'keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post',
    all_testdata,
)
def test_inorder_traversal(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_inorder() == expected_in


@pytest.mark.parametrize(
    'keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post',
    all_testdata,
)
def test_reverse_inorder_traversal(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_reverse_inorder() == expected_rev_in


@pytest.mark.parametrize(
    'keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post',
    all_testdata,
)
def test_postorder_traversal(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_postorder() == expected_post


@pytest.mark.parametrize(
    'keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post',
    all_testdata,
)
def test_reverse_postorder_traversal(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_reverse_postorder() == expected_rev_post


@pytest.mark.parametrize('keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post', all_testdata)
def test_inorder_is_strictly_sorted(keys: list[int], expected_pre, expected_in, expected_post, expected_rev_pre, expected_rev_in, expected_rev_post) -> None:
    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.get_inorder() == sorted(keys)
    assert bst.get_reverse_inorder() == sorted(keys, reverse=True)


def test_empty_tree() -> None:
    # 1. Построение из пустого списка ключей возвращает пустое дерево
    bst_from_empty = BinarySearchTree.build_from_preorder_keys([])
    assert bst_from_empty is not None
    assert bst_from_empty.root is None
    assert bst_from_empty.get_preorder() == []
    assert bst_from_empty.get_reverse_preorder() == []
    assert bst_from_empty.get_inorder() == []
    assert bst_from_empty.get_reverse_inorder() == []
    assert bst_from_empty.get_postorder() == []
    assert bst_from_empty.get_reverse_postorder() == []

    # 2. Дерево с root = None возвращает пустые списки обходов
    empty_tree = BinarySearchTree(None)
    assert empty_tree.get_preorder() == []
    assert empty_tree.get_reverse_preorder() == []
    assert empty_tree.get_inorder() == []
    assert empty_tree.get_reverse_inorder() == []
    assert empty_tree.get_postorder() == []
    assert empty_tree.get_reverse_postorder() == []


def test_insert_into_empty_tree() -> None:
    bst = BinarySearchTree()
    assert bst.root is None

    bst.insert(10)
    assert bst.root is not None
    assert bst.root.key == 10
    assert bst.root.left is None
    assert bst.root.right is None
    assert bst.get_inorder() == [10]


def test_insert_into_existing_tree() -> None:
    # Исходное дерево: [8, 3, 1, 6, 4, 7, 10, 14, 13]
    initial_keys = [8, 3, 1, 6, 4, 7, 10, 14, 13]
    bst = BinarySearchTree.build_from_preorder_keys(initial_keys)

    # Вставляем новые элементы: 2 (в левое поддерево), 9, 15 (в правое поддерево)
    bst.insert(2)
    bst.insert(9)
    bst.insert(15)

    expected_inorder = sorted(initial_keys + [2, 9, 15])
    assert bst.get_inorder() == expected_inorder
    assert bst.get_reverse_inorder() == sorted(expected_inorder, reverse=True)


def test_insert_duplicate_key() -> None:
    # Дубликаты в BST не должны добавлять новые узлы
    bst = BinarySearchTree.build_from_preorder_keys([5, 3, 7])

    bst.insert(3)
    bst.insert(5)
    bst.insert(7)

    assert bst.get_inorder() == [3, 5, 7]


@pytest.mark.parametrize('keys,expected_pre,expected_in,expected_post,expected_rev_pre,expected_rev_in,expected_rev_post', all_testdata)
def test_build_by_insertions_matches_preorder_build(
    keys: list[int],
    expected_pre: list[int],
    expected_in: list[int],
    expected_post: list[int],
    expected_rev_pre: list[int],
    expected_rev_in: list[int],
    expected_rev_post: list[int],
) -> None:
    tree_by_insert = BinarySearchTree()
    for key in keys:
        tree_by_insert.insert(key)

    assert tree_by_insert.get_preorder() == expected_pre
    assert tree_by_insert.get_reverse_preorder() == expected_rev_pre
    assert tree_by_insert.get_inorder() == expected_in
    assert tree_by_insert.get_reverse_inorder() == expected_rev_in
    assert tree_by_insert.get_postorder() == expected_post
    assert tree_by_insert.get_reverse_postorder() == expected_rev_post


def test_large_skewed_tree_no_recursion_error() -> None:
    """
    Тест на большое вырожденное дерево (10^4 узлов).
    Рекурсивный обход упал бы с RecursionError (лимит по умолчанию 1000).
    Итеративные методы со стеком должны успешно завершиться без падений.
    """
    n = 10_000
    keys = list(range(n))  # Вырожденное вправо дерево

    bst = BinarySearchTree.build_from_preorder_keys(keys)
    assert bst.root is not None

    pre = bst.get_preorder()
    assert len(pre) == n
    assert pre[:3] == [0, 1, 2]
    assert pre[-1] == n - 1

    rev_pre = bst.get_reverse_preorder()
    assert len(rev_pre) == n

    inorder = bst.get_inorder()
    assert len(inorder) == n
    assert inorder == keys

    rev_inorder = bst.get_reverse_inorder()
    assert len(rev_inorder) == n
    assert rev_inorder == keys[::-1]

    post = bst.get_postorder()
    assert len(post) == n
    assert post == keys[::-1]

    rev_post = bst.get_reverse_postorder()
    assert len(rev_post) == n
    assert rev_post == keys[::-1]
