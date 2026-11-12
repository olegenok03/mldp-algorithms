import os
import random
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import pytest
from avl_tree import AVL, AVLNode


# =====================================================================
# 1. Тесты поиска (search, __contains__)
# =====================================================================

def test_search_empty_tree() -> None:
    tree = AVL()
    assert tree.search(10) is None
    assert 10 not in tree


def test_search_existing_and_missing_keys() -> None:
    tree = AVL()
    keys = [20, 10, 30, 5, 15, 25, 35]
    for k in keys:
        tree.insert(k)

    # Проверка существующих ключей
    for k in keys:
        node = tree.search(k)
        assert node is not None
        assert node.key == k
        assert k in tree

    # Проверка отсутствующих ключей
    for missing in [-100, 0, 7, 18, 42, 999]:
        assert tree.search(missing) is None
        assert missing not in tree


# =====================================================================
# 2. Тесты базовой вставки и 4-х типов вращений (LL, RR, LR, RL)
# =====================================================================

def test_insert_empty_and_single() -> None:
    tree = AVL()
    assert tree.root is None
    assert tree.inorder() == []

    tree.insert(42)
    assert tree.root is not None
    assert tree.root.key == 42
    assert tree.root.height == 1
    assert tree.inorder() == [42]
    assert tree.is_valid_avl()


def test_insert_duplicate_keys() -> None:
    tree = AVL()
    tree.insert(10)
    tree.insert(10)
    tree.insert(10)

    assert tree.inorder() == [10]
    assert tree.root is not None and tree.root.height == 1
    assert tree.is_valid_avl()


def test_rotation_left_left_ll() -> None:
    # Вставка в нисходящем порядке вызывает малое правое вращение (LL)
    tree = AVL()
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    # Ожидаемый корень 20, левый потомок 10, правый 30
    assert tree.root is not None
    assert tree.root.key == 20
    assert tree.root.left is not None and tree.root.left.key == 10
    assert tree.root.right is not None and tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.is_valid_avl()


def test_rotation_right_right_rr() -> None:
    # Вставка в возрастающем порядке вызывает малое левое вращение (RR)
    tree = AVL()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)

    # Ожидаемый корень 20, левый потомок 10, правый 30
    assert tree.root is not None
    assert tree.root.key == 20
    assert tree.root.left is not None and tree.root.left.key == 10
    assert tree.root.right is not None and tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.is_valid_avl()


def test_rotation_left_right_lr() -> None:
    # Большой правый поворот (Left-Right)
    tree = AVL()
    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.root is not None
    assert tree.root.key == 20
    assert tree.root.left is not None and tree.root.left.key == 10
    assert tree.root.right is not None and tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.is_valid_avl()


def test_rotation_right_left_rl() -> None:
    # Большой левый поворот (Right-Left)
    tree = AVL()
    tree.insert(10)
    tree.insert(30)
    tree.insert(20)

    assert tree.root is not None
    assert tree.root.key == 20
    assert tree.root.left is not None and tree.root.left.key == 10
    assert tree.root.right is not None and tree.root.right.key == 30
    assert tree.root.height == 2
    assert tree.is_valid_avl()


# =====================================================================
# 3. Тесты удаления (delete)
# =====================================================================

def test_delete_from_empty_and_missing() -> None:
    tree = AVL()
    tree.delete(100)  # Не должно падать на пустом дереве
    assert tree.root is None

    tree.insert(10)
    tree.delete(999)  # Отсутствующий ключ
    assert tree.inorder() == [10]
    assert tree.is_valid_avl()


def test_delete_leaf_node() -> None:
    tree = AVL()
    for k in [20, 10, 30]:
        tree.insert(k)

    tree.delete(10)  # Удаление листа слева
    assert 10 not in tree
    assert tree.inorder() == [20, 30]
    assert tree.is_valid_avl()

    tree.delete(30)  # Удаление листа справа
    assert 30 not in tree
    assert tree.inorder() == [20]
    assert tree.is_valid_avl()


def test_delete_node_with_one_child() -> None:
    tree = AVL()
    # Дерево: 20 -> left 10 -> left 5 (после балансировки: корень 10, дети 5 и 20)
    # Построим узел с одним потомком:
    for k in [20, 10, 30, 25]:
        tree.insert(k)

    # Узел 30 имеет только левого потомка 25
    tree.delete(30)
    assert 30 not in tree
    assert 25 in tree
    assert tree.inorder() == [10, 20, 25]
    assert tree.is_valid_avl()


def test_delete_node_with_two_children() -> None:
    tree = AVL()
    keys = [50, 25, 75, 10, 30, 60, 80]
    for k in keys:
        tree.insert(k)

    # Удаляем корень 50 (у него 2 потомка)
    tree.delete(50)
    assert 50 not in tree
    assert tree.inorder() == [10, 25, 30, 60, 75, 80]
    assert tree.is_valid_avl()

    # Удаляем узел 75 (у него 2 потомка: 60 и 80)
    tree.delete(75)
    assert 75 not in tree
    assert tree.inorder() == [10, 25, 30, 60, 80]
    assert tree.is_valid_avl()


def test_delete_all_nodes_until_empty() -> None:
    tree = AVL()
    keys = [15, 10, 20, 8, 12, 17, 25]
    for k in keys:
        tree.insert(k)

    for k in keys:
        tree.delete(k)
        assert k not in tree
        assert tree.is_valid_avl()

    assert tree.root is None
    assert tree.inorder() == []


def test_init_with_root_validation() -> None:
    # 1. Корректный корень принимается
    valid_root = AVLNode(10)
    valid_root.left = AVLNode(5)
    valid_root.right = AVLNode(15)
    valid_root.height = 2
    tree = AVL(valid_root)
    assert tree.root is not None and tree.root.key == 10

    # 2. Некорректный корень (нарушение BST) вызывает ValueError
    invalid_bst_root = AVLNode(10)
    invalid_bst_root.left = AVLNode(20)  # левый больше корня!
    with pytest.raises(ValueError, match='violates AVL invariants'):
        AVL(invalid_bst_root)

    # 3. Некорректный корень (нарушение баланса) вызывает ValueError
    unbalanced_root = AVLNode(10)
    unbalanced_root.left = AVLNode(5)
    unbalanced_root.left.left = AVLNode(2)
    unbalanced_root.height = 3
    unbalanced_root.left.height = 2
    with pytest.raises(ValueError, match='violates AVL invariants'):
        AVL(unbalanced_root)


def test_delete_rotation_ll() -> None:
    # Удаление узла 30 оставляет корень 20 с левым ребенком 10 (h=2, BF >= 0)
    # Вызывается малое правое вращение (LL)
    tree = AVL()
    for k in [20, 10, 30, 5]:
        tree.insert(k)

    tree.delete(30)
    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.left is not None and tree.root.left.key == 5
    assert tree.root.right is not None and tree.root.right.key == 20
    assert tree.root.height == 2


def test_delete_rotation_rr() -> None:
    # Удаление узла 10 оставляет корень 20 с правым ребенком 30 (h=2, BF <= 0)
    # Вызывается малое левое вращение (RR)
    tree = AVL()
    for k in [20, 10, 30, 40]:
        tree.insert(k)

    tree.delete(10)
    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.key == 30
    assert tree.root.left is not None and tree.root.left.key == 20
    assert tree.root.right is not None and tree.root.right.key == 40
    assert tree.root.height == 2


def test_delete_rotation_lr() -> None:
    # Удаление узла 30 оставляет корень 20 с левым ребенком 10, у которого BF < 0 (правый потомок 15)
    # Вызывается большой правый поворот (LR)
    tree = AVL()
    for k in [20, 10, 30, 15]:
        tree.insert(k)

    tree.delete(30)
    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.key == 15
    assert tree.root.left is not None and tree.root.left.key == 10
    assert tree.root.right is not None and tree.root.right.key == 20
    assert tree.root.height == 2


def test_delete_rotation_rl() -> None:
    # Удаление узла 10 оставляет корень 20 с правым ребенком 30, у которого BF > 0 (левый потомок 25)
    # Вызывается большой левый поворот (RL)
    tree = AVL()
    for k in [20, 10, 30, 25]:
        tree.insert(k)

    tree.delete(10)
    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.key == 25
    assert tree.root.left is not None and tree.root.left.key == 20
    assert tree.root.right is not None and tree.root.right.key == 30
    assert tree.root.height == 2


def test_delete_cascading_multiple_rotations() -> None:
    # Каскадная ребалансировка: удаление одного узла провоцирует цепочку
    # независимых вращений на разных уровнях дерева по пути к корню
    tree = AVL()
    keys = [5, 6, 3, 9, 8, 10, 2, 1, 7, 11, 4, 12]
    for k in keys:
        tree.insert(k)

    # Исходный корень 5, высота 5
    assert tree.root is not None and tree.root.key == 5
    assert tree.root.height == 5

    # Удаление листа 1 провоцирует:
    # 1. Левый поворот вокруг узла 2 (уменьшает высоту левого поддерева до 2)
    # 2. Каскадный левый поворот вокруг корня 5 (делает 8 новым корнем дерева)
    tree.delete(1)

    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.key == 8
    assert tree.root.height == 4
    assert tree.root.left is not None and tree.root.left.key == 5
    assert tree.root.right is not None and tree.root.right.key == 10


# =====================================================================
# 4. Нагрузочные и стресс-тесты
# =====================================================================

def test_strictly_ascending_insertions_height_bound() -> None:
    # В обычном BST вставка 1..100 дает вырожденный список высотой 100.
    # В AVL-дереве высота строго ограничена ~ 1.44 * log2(N + 2).
    # Для N=100 высота AVL <= 8.
    tree = AVL()
    for i in range(1, 101):
        tree.insert(i)

    assert tree.inorder() == list(range(1, 101))
    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.height <= 8


def test_strictly_descending_insertions_height_bound() -> None:
    tree = AVL()
    for i in range(100, 0, -1):
        tree.insert(i)

    assert tree.inorder() == list(range(1, 101))
    assert tree.is_valid_avl()
    assert tree.root is not None
    assert tree.root.height <= 8


def test_randomized_stress_operations() -> None:
    # Стресс-тест со случайными вставками и удалениями
    random.seed(42)
    tree = AVL()
    active_keys: set[int] = set()

    # 1. Случайная вставка 200 элементов
    for _ in range(200):
        val = random.randint(-500, 500)
        tree.insert(val)
        active_keys.add(val)
        assert tree.is_valid_avl()

    assert tree.inorder() == sorted(active_keys)

    # 2. Случайное удаление половины элементов
    keys_to_delete = random.sample(list(active_keys), len(active_keys) // 2)
    for val in keys_to_delete:
        tree.delete(val)
        active_keys.remove(val)
        assert tree.is_valid_avl()

    assert tree.inorder() == sorted(active_keys)


def test_visualize_output() -> None:
    tree = AVL()
    assert tree.visualize() == '<Empty Tree>'

    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    vis = tree.visualize()
    assert '10 (h=2)' in vis
    assert '5 (h=1)' in vis
    assert '15 (h=1)' in vis

