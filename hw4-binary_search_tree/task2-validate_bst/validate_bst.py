import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from binary_search_tree import BinarySearchTree, TreeNode


def validate_bst(tree: BinarySearchTree) -> bool:
    """
    Проверяет, является ли бинарное дерево корректным бинарным деревом поиска (BST).
    """
    curr = tree.root
    tree_stack: list[TreeNode] = []
    prev_key: int | None = None

    while curr is not None or tree_stack:
        if curr is not None:
            tree_stack.append(curr)
            curr = curr.left
        else:
            curr = tree_stack.pop()
            # В корректном BST ключи в порядке in-order строго возрастают
            if prev_key is not None and curr.key <= prev_key:
                return False
            prev_key = curr.key
            curr = curr.right

    return True


if __name__ == '__main__':
    # Пример 1: Корректное BST
    valid_bst = BinarySearchTree.build_from_preorder_keys([4, 2, 1, 3, 6, 5, 7])
    print('Valid BST:', validate_bst(valid_bst))  # True

    # Пример 2: Некорректное дерево (нарушение в правом поддереве)
    #        5
    #       / \
    #      1   4
    #         / \
    #        3   6
    invalid_root = TreeNode(5)
    invalid_root.left = TreeNode(1)
    invalid_root.right = TreeNode(4)
    invalid_root.right.left = TreeNode(3)
    invalid_root.right.right = TreeNode(6)
    invalid_tree = BinarySearchTree(invalid_root)
    print('Invalid BST:', validate_bst(invalid_tree))  # False
