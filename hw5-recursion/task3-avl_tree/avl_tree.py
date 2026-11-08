from __future__ import annotations


class AVLNode:
    """Узел AVL-дерева с хранением высоты поддерева."""

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height: int = 1

    def __repr__(self) -> str:
        return f'AVLNode(key={self.key}, h={self.height})'


class AVL:
    """
    Самобалансирующееся двоичное дерево поиска (AVL-дерево).
    Поддерживает операции вставки, удаления и поиска за O(log N).
    """

    def __init__(self, root: AVLNode | None = None) -> None:
        self.root: AVLNode | None = root

    # =========================================================================
    # Вспомогательные методы работы с высотой и балансом
    # =========================================================================

    @staticmethod
    def get_height(node: AVLNode | None) -> int:
        """Возвращает высоту поддерева с корнем в node (0 для None)."""
        return node.height if node is not None else 0

    def get_balance(self, node: AVLNode | None) -> int:
        """
        Фактор баланса (balance factor): разность высот левого и правого поддеревьев.
        Для сбалансированного узла AVL значение принадлежит {-1, 0, 1}.
        """
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        """Пересчитывает высоту узла на основе высот его потомков."""
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # =========================================================================
    # Балансировочные вращения (Rotations)
    # =========================================================================

    def right_rotate(self, y: AVLNode) -> AVLNode:
        r"""
        Малое правое вращение вокруг узла y:
             y                 x
            / \               / \
           x   T3    -->     T1  y
          / \                   / \
         T1  T2                T2  T3
        """
        x = y.left
        assert x is not None
        t2 = x.right

        # Переброс связей
        x.right = y
        y.left = t2

        # Пересчет высот: сначала опущенного y, затем поднятого x
        self._update_height(y)
        self._update_height(x)

        return x

    def left_rotate(self, x: AVLNode) -> AVLNode:
        r"""
        Малое левое вращение вокруг узла x:
           x                     y
          / \                   / \
         T1  y       -->       x   T3
            / \               / \
           T2  T3            T1  T2
        """
        y = x.right
        assert y is not None
        t2 = y.left

        # Переброс связей
        y.left = x
        x.right = t2

        # Пересчет высот: сначала опущенного x, затем поднятого y
        self._update_height(x)
        self._update_height(y)

        return y

    # =========================================================================
    # 1. Вставка (Insert)
    # =========================================================================

    def insert(self, key: int) -> None:
        """Вставляет ключ key в AVL-дерево и восстанавливает баланс."""
        self.root = self._insert(self.root, key)

    def _insert(self, node: AVLNode | None, key: int) -> AVLNode:
        # 1. Стандартная рекурсивная вставка в BST
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Дубликаты в стандартном множестве игнорируются
            return node

        # 2. Обновление высоты текущего узла на обратном ходе рекурсии
        self._update_height(node)

        # 3. Вычисление фактора баланса для проверки нарушения инварианта AVL
        balance = self.get_balance(node)

        # 4. Балансировка при нарушении (4 классических случая):

        # Left-Left (LL): перевес слева, новый ключ меньше левого ребенка
        if balance > 1 and node.left is not None and key < node.left.key:
            return self.right_rotate(node)

        # Right-Right (RR): перевес справа, новый ключ больше правого ребенка
        if balance < -1 and node.right is not None and key > node.right.key:
            return self.left_rotate(node)

        # Left-Right (LR): большой правый поворот (левое вращение ребенка + правое вращение узла)
        if balance > 1 and node.left is not None and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right-Left (RL): большой левый поворот (правое вращение ребенка + левое вращение узла)
        if balance < -1 and node.right is not None and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # =========================================================================
    # 2. Удаление (Delete)
    # =========================================================================

    def delete(self, key: int) -> None:
        """Удаляет ключ key из AVL-дерева и восстанавливает баланс."""
        self.root = self._delete(self.root, key)

    def _delete(self, node: AVLNode | None, key: int) -> AVLNode | None:
        # 1. Стандартный рекурсивный спуск в BST для поиска удаляемого узла
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Найден удаляемый узел:
            # Случай 1: 0 или 1 потомок
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Случай 2: 2 потомка — ищем in-order преемника (минимум в правом поддереве)
            successor = self._min_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        # 2. Обновление высоты узла
        self._update_height(node)

        # 3. Вычисление фактора баланса
        balance = self.get_balance(node)

        # 4. Балансировка после удаления (4 случая на основе баланса потомков):

        # Left-Left (LL)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Left-Right (LR)
        if balance > 1 and self.get_balance(node.left) < 0:
            assert node.left is not None
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right-Right (RR)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Right-Left (RL)
        if balance < -1 and self.get_balance(node.right) > 0:
            assert node.right is not None
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    @staticmethod
    def _min_node(node: AVLNode) -> AVLNode:
        """Возвращает узел с минимальным ключом в данном поддереве."""
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    # =========================================================================
    # 3. Поиск (Search)
    # =========================================================================

    def search(self, key: int) -> AVLNode | None:
        """Ищет узел по ключу. Возвращает AVLNode или None, если ключ не найден."""
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return curr
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def __contains__(self, key: int) -> bool:
        """Поддержка оператора `key in tree`."""
        return self.search(key) is not None

    # =========================================================================
    # Утилиты проверки и визуализации
    # =========================================================================

    def inorder(self) -> list[int]:
        """Симметричный обход (In-order traversal). Возвращает ключи по возрастанию."""
        result: list[int] = []

        def _traverse(node: AVLNode | None) -> None:
            if node is not None:
                _traverse(node.left)
                result.append(node.key)
                _traverse(node.right)

        _traverse(self.root)
        return result

    def is_valid_avl(self) -> bool:
        """
        Проверяет строгие инварианты AVL-дерева:
        1. BST-инвариант (in-order строго возрастает);
        2. Корректность высот: height == 1 + max(h_left, h_right);
        3. Баланс каждого узла лежит в диапазоне {-1, 0, 1}.
        """
        # 1. Проверка отсортированности ключей
        keys = self.inorder()
        if keys != sorted(set(keys)):
            return False

        # 2. Проверка баланса и высот в каждом узле
        def _check(node: AVLNode | None) -> tuple[bool, int]:
            if node is None:
                return True, 0

            left_valid, left_h = _check(node.left)
            right_valid, right_h = _check(node.right)

            if not left_valid or not right_valid:
                return False, 0

            if abs(left_h - right_h) > 1:
                return False, 0

            expected_h = 1 + max(left_h, right_h)
            if node.height != expected_h:
                return False, 0

            return True, expected_h

        valid, _ = _check(self.root)
        return valid

    def visualize(self) -> str:
        """Строковое псевдографическое представление дерева для отладки."""
        if not self.root:
            return '<Empty Tree>'

        lines: list[str] = []

        def _build(node: AVLNode | None, prefix: str = '', is_left: bool = True) -> None:
            if node is not None:
                lines.append(f'{prefix}{"|-- " if is_left else "\\-- "}{node.key} (h={node.height})')
                next_prefix = prefix + ('|   ' if is_left else '    ')
                if node.left or node.right:
                    if node.left:
                        _build(node.left, next_prefix, True)
                    else:
                        lines.append(f'{next_prefix}|-- None')
                    if node.right:
                        _build(node.right, next_prefix, False)
                    else:
                        lines.append(f'{next_prefix}\\-- None')

        lines.append(f'{self.root.key} (h={self.root.height})')
        if self.root.left or self.root.right:
            if self.root.left:
                _build(self.root.left, '', True)
            else:
                lines.append('|-- None')
            if self.root.right:
                _build(self.root.right, '', False)
            else:
                lines.append('\\-- None')

        return '\n'.join(lines)


if __name__ == '__main__':
    tree = AVL()
    for val in [10, 20, 30, 40, 50, 25]:
        tree.insert(val)
    print('AVL Tree structure:')
    print(tree.visualize())
    print('In-order:', tree.inorder())
    print('Is valid AVL:', tree.is_valid_avl())
