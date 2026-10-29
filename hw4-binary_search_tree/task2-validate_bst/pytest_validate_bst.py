import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from binary_search_tree import BinarySearchTree, TreeNode
from validate_bst import validate_bst

# Наборы корректных деревьев
testdata_valid_bst = [
    # Пустое дерево и один узел
    [],
    [42],
    # 2 узла
    [10, 5],
    [10, 15],
    # Вырожденные деревья ("бамбук")
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    # Зигзаг
    [5, 1, 4, 2, 3],
    # Сбалансированные и разветвленные деревья
    [4, 2, 1, 3, 6, 5, 7],
    [8, 3, 1, 6, 4, 7, 10, 14, 13],
    [0, -10, -20, -5, 10, 5, 20],
]


@pytest.mark.parametrize('keys', testdata_valid_bst)
def test_valid_bst_from_preorder(keys: list[int]) -> None:
    tree = BinarySearchTree.build_from_preorder_keys(keys)
    assert validate_bst(tree) is True


def test_empty_tree() -> None:
    # Краевой случай: пустое дерево
    empty_tree = BinarySearchTree()
    assert validate_bst(empty_tree) is True


def test_invalid_bst_direct_children_violations() -> None:
    # 1. Левый ребенок больше родителя
    root1 = TreeNode(5)
    root1.left = TreeNode(10)
    assert validate_bst(BinarySearchTree(root1)) is False

    # 2. Правый ребенок меньше родителя
    root2 = TreeNode(5)
    root2.right = TreeNode(2)
    assert validate_bst(BinarySearchTree(root2)) is False


def test_invalid_bst_duplicate_keys() -> None:
    # Дубликаты запрещены в строгом BST
    root1 = TreeNode(5)
    root1.left = TreeNode(5)
    assert validate_bst(BinarySearchTree(root1)) is False

    root2 = TreeNode(5)
    root2.right = TreeNode(5)
    assert validate_bst(BinarySearchTree(root2)) is False


def test_invalid_bst_global_subtree_violations() -> None:
    # Классический случай: каждый узел больше/меньше своих прямых потомков,
    # но нарушается глобальное свойство поддерева:
    #
    #         10
    #        /  \
    #       5    15
    #           /  \
    #          6    20
    #
    # Узел 6 меньше родителя 15 (локально верно), но находится в правом
    # поддереве корня 10 (6 < 10 — глобально неверно).
    root1 = TreeNode(10)
    root1.left = TreeNode(5)
    root1.right = TreeNode(15)
    root1.right.left = TreeNode(6)
    root1.right.right = TreeNode(20)
    assert validate_bst(BinarySearchTree(root1)) is False

    # Аналогично в левом поддереве: узел 12 больше корня 10
    #         10
    #        /  \
    #       5    15
    #      / \
    #     2   12
    root2 = TreeNode(10)
    root2.left = TreeNode(5)
    root2.right = TreeNode(15)
    root2.left.left = TreeNode(2)
    root2.left.right = TreeNode(12)
    assert validate_bst(BinarySearchTree(root2)) is False


def test_large_valid_and_invalid_bst() -> None:
    # Большое корректное дерево
    large_keys = list(range(100))
    tree = BinarySearchTree()
    for k in large_keys:
        tree.insert(k)
    assert validate_bst(tree) is True

    # Испортим один узел в самом конце
    curr = tree.root
    while curr.right is not None:
        curr = curr.right
    curr.left = TreeNode(500)  # Левый потомок 500 для узла 99
    assert validate_bst(tree) is False
