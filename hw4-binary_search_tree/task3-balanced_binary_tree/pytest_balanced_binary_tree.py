import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from balanced_binary_tree import is_balanced
from binary_search_tree import BinarySearchTree, TreeNode

# Набор сбалансированных деревьев (построение через preorder ключи BST)
testdata_balanced_preorder = [
    # Пустое дерево
    [],
    # 1 узел
    [42],
    # 2 узла
    [10, 5],
    [10, 15],
    # 3 узла сбалансированные
    [2, 1, 3],
    # Полное бинарное дерево (высота 3)
    [4, 2, 1, 3, 6, 5, 7],
    # Почти полное дерево
    [4, 2, 1, 3, 6, 5],
    # Сбалансированное дерево из 8 узлов
    [5, 2, 1, 3, 7, 6, 8, 9],
]

# Набор несбалансированных деревьев
testdata_unbalanced_preorder = [
    # Вырожденные ("бамбук")
    [3, 2, 1],
    [1, 2, 3],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    # Зигзаг
    [5, 1, 4, 2, 3],
    # Дерево сбалансировано у корня (3 vs 3), но узел 10 несбалансирован (0 vs 2)
    [8, 3, 1, 6, 4, 7, 10, 14, 13],
]


@pytest.mark.parametrize('keys', testdata_balanced_preorder)
def test_balanced_trees(keys: list[int]) -> None:
    tree = BinarySearchTree.build_from_preorder_keys(keys)
    assert is_balanced(tree) is True


@pytest.mark.parametrize('keys', testdata_unbalanced_preorder)
def test_unbalanced_trees(keys: list[int]) -> None:
    tree = BinarySearchTree.build_from_preorder_keys(keys)
    assert is_balanced(tree) is False


def test_empty_tree() -> None:
    # Единственный краевой случай: пустое дерево
    empty_tree = BinarySearchTree()
    assert is_balanced(empty_tree) is True


def test_arbitrary_binary_trees_not_bst() -> None:
    # Пример 1: Сбалансированное дерево с дубликатами
    #        1
    #       / \
    #      2   2
    #     / \
    #    3   3
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(2)
    root1.left.left = TreeNode(3)
    root1.left.right = TreeNode(3)
    assert is_balanced(BinarySearchTree(root1)) is True

    # Пример 2: Несбалансированное дерево
    #         1
    #        / \
    #       2   2
    #      / \
    #     3   3
    #    / \
    #   4   4
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(2)
    root2.left.left = TreeNode(3)
    root2.left.right = TreeNode(3)
    root2.left.left.left = TreeNode(4)
    root2.left.left.right = TreeNode(4)
    assert is_balanced(BinarySearchTree(root2)) is False


def test_subtrees_imbalance() -> None:
    # Случай: корень имеет разницу высот <= 1, но в глубине поддерева есть дисбаланс:
    #             1
    #           /   \
    #          2     3
    #         / \     \
    #        4   5     6
    #       /           \
    #      7             8
    #     /
    #    9
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.left.left.left = TreeNode(7)
    root.left.left.left.left = TreeNode(9)

    root.right.right = TreeNode(6)
    root.right.right.right = TreeNode(8)

    assert is_balanced(BinarySearchTree(root)) is False
