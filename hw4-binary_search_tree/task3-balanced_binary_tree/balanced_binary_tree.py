import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from binary_search_tree import BinarySearchTree, TreeNode


def is_balanced_recursive(tree: BinarySearchTree) -> bool:
    """
    Определяет, является ли бинарное дерево сбалансированным по высоте (рекурсивный вариант).
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


def is_balanced_iterative(tree: BinarySearchTree) -> bool:
    """
    Определяет, является ли бинарное дерево сбалансированным по высоте (итеративный вариант).
    """
    if tree.root is None:
        return True

    # Элемент стека: [node, left_height, state]
    # state:
    #   0 - вход в узел (перед спуском в левое поддерево)
    #   1 - возврат из левого поддерева (перед спуском в правое)
    #   2 - возврат из обоих поддеревьев (проверка баланса и расчет высоты)
    stack: list[list] = [[tree.root, 0, 0]]
    ret_height = 0

    while stack:
        frame = stack[-1]
        node, left_height, state = frame

        if state == 0:
            frame[2] = 1
            if node.left is not None:
                stack.append([node.left, 0, 0])
            else:
                ret_height = 0
        elif state == 1:
            frame[1] = ret_height
            frame[2] = 2
            if node.right is not None:
                stack.append([node.right, 0, 0])
            else:
                ret_height = 0
        else:
            right_height = ret_height
            if abs(left_height - right_height) > 1:
                return False
            ret_height = 1 + max(left_height, right_height)
            stack.pop()

    return True


if __name__ == '__main__':
    # Пример 1: Сбалансированное дерево
    balanced_tree = BinarySearchTree.build_from_preorder_keys([4, 2, 1, 3, 6, 5, 7])
    print('Balanced (rec):', is_balanced_recursive(balanced_tree))  # True
    print('Balanced (iter):', is_balanced_iterative(balanced_tree))  # True

    # Пример 2: Дерево с дисбалансом в узле 10
    unbalanced_tree = BinarySearchTree.build_from_preorder_keys(
        [8, 3, 1, 6, 4, 7, 10, 14, 13]
    )
    print('Unbalanced (rec):', is_balanced_recursive(unbalanced_tree))  # False
    print('Unbalanced (iter):', is_balanced_iterative(unbalanced_tree))  # False
