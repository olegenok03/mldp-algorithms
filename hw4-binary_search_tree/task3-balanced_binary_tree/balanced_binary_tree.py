import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from binary_search_tree import BinarySearchTree, TreeNode


def is_balanced(tree: BinarySearchTree) -> bool:
    """
    Определяет, является ли бинарное дерево поиска сбалансированным по высоте.

    Бинарное дерево считается сбалансированным по высоте, если для каждого узла
    высоты его левого и правого поддеревьев отличаются не более чем на 1.
    """

    def check_height(node: TreeNode | None) -> int:
        if node is None:
            return 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1

        right_height = check_height(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return 1 + max(left_height, right_height)

    return check_height(tree.root) != -1


if __name__ == '__main__':
    # Пример 1: Сбалансированное дерево
    balanced_tree = BinarySearchTree.build_from_preorder_keys([4, 2, 1, 3, 6, 5, 7])
    print('Balanced:', is_balanced(balanced_tree))  # True

    # Пример 2: Несбалансированное дерево
    unbalanced_tree = BinarySearchTree.build_from_preorder_keys([3, 2, 1])
    print('Unbalanced:', is_balanced(unbalanced_tree))  # False
