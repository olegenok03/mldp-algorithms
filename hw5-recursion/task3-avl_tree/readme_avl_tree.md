# Задание 3. AVL-tree

## Описание решения

В задаче требуется реализовать класс `AVL`, представляющий собой сбалансированное по высоте двоичное дерево поиска (АВЛ-дерево, названное в честь советских математиков Г. М. Адельсона-Вельского и Е. М. Ландиса).

### Инварианты AVL-дерева

1. **Инвариант двоичного дерева поиска (BST):**
   Для любого узла с ключом $K$:
   - Все ключи в левом поддереве строго меньше $K$.
   - Все ключи в правом поддереве строго больше $K$.

2. **Инвариант баланса по высоте:**
   Для **каждого** узла дерева разность высот его левого и правого поддеревьев (фактор баланса, **Balance Factor**) по модулю не превосходит 1:
   
   $$BF(node) = h(node.left) - h(node.right) \in \{-1, 0, 1\}$$

   где высота пустого поддерева $h(\text{None}) = 0$, а листа — $1$.

3. **Гарантия логарифмической высоты:**
   Благодаря балансировке высота дерева из $N$ элементов строго ограничена:
   
   $$h < 1.4404 \log_2(N + 2) - 0.328 \implies h = O(\log N)$$
   
   Это гарантирует, что дерево никогда не вырождается в связный список (в отличие от наивного BST), а операции поиска, вставки и удаления выполняются строго за **$O(\log N)$** в худшем случае.

---

## Балансировочные вращения (Rotations)

При вставке или удалении фактор баланса некоторого предка может стать равным $+2$ или $-2$. Нарушение устраняется с помощью локальных перестановок ссылок за $O(1)$ — вращений. 

Поскольку вставка и удаление реализованы **рекурсивно**, проверка и восстановление баланса происходят на **обратном ходе рекурсии** (снизу вверх) от точки изменения к корню дерева.

### 1. Малое правое вращение (Right Rotation / LL-случай)
Возникает, когда левое поддерево выше правого ($BF = +2$), и новый элемент добавлен в левое поддерево левого потомка ($BF(left) \ge 0$):

```text
       y                               x
      / \                             / \
     x   T3     Right Rotate(y)      T1  y
    / \         -------------->         / \
   T1  T2                              T2  T3
```

### 2. Малое левое вращение (Left Rotation / RR-случай)
Возникает, когда правое поддерево выше левого ($BF = -2$), и новый элемент добавлен в правое поддерево правого потомка ($BF(right) \le 0$):

```text
     x                                 y
    / \                               / \
   T1  y        Left Rotate(x)       x   T3
      / \       ------------->      / \
     T2  T3                        T1  T2
```

### 3. Большое правое вращение (Left-Right Rotation / LR-случай)
Возникает, когда $BF = +2$, а левый потомок перевешивает вправо ($BF(left) < 0$):
1. Малое левое вращение для левого потомка: `node.left = left_rotate(node.left)`.
2. Малое правое вращение для текущего узла: `return right_rotate(node)`.

```text
       z                      z                    x
      / \   Left Rotate(y)   / \  Right Rotate(z) / \
     y   T4 ------------->  x   T4 ------------> y   z
    / \                    / \                  / \ / \
   T1  x                  y   T3               T1 T2 T3 T4
      / \                / \
     T2  T3             T1  T2
```

### 4. Большое левое вращение (Right-Left Rotation / RL-случай)
Возникает, когда $BF = -2$, а правый потомок перевешивает влево ($BF(right) > 0$):
1. Малое правое вращение для правого потомка: `node.right = right_rotate(node.right)`.
2. Малое левое вращение для текущего узла: `return left_rotate(node)`.

---

## Поддерживаемые операции

### 1. Поиск (`search(key) -> AVLNode | None`, `key in tree`)
* Выполняется стандартный спуск по BST:
  * Если `key == curr.key` — узел найден.
  * Если `key < curr.key` — идем влево.
  * Если `key > curr.key` — идем вправо.
* В силу гарантированной высоты $h = O(\log N)$ поиск всегда занимает не более $O(\log N)$ шагов.

### 2. Вставка (`insert(key) -> None`)
* Рекурсивный спуск в подходящий лист по правилам BST.
* Создание нового `AVLNode(key)`.
* **На обратном ходе рекурсии:**
  1. Пересчет высоты узла: `node.height = 1 + max(h(left), h(right))`.
  2. Проверка фактора баланса: `balance = h(left) - h(right)`.
  3. Если $|balance| > 1$, выполняется соответствующее вращение (LL, RR, LR или RL).

### 3. Удаление (`delete(key) -> None`)
* Рекурсивный спуск для поиска удаляемого ключа.
* При нахождении узла обрабатываются 3 случая:
  1. **Лист (0 потомков):** узел просто удаляется (возвращается `None`).
  2. **Один потомок:** узел замещается своим единственным дочерним поддеревом (`node.left` или `node.right`).
  3. **Два потомка:** находится **in-order преемник** (минимальный узел в правом поддереве), его ключ копируется в текущий узел, после чего преемник рекурсивно удаляется из правого поддерева.
* **На обратном ходе рекурсии:** пересчет высоты и ребалансировка (в отличие от вставки, удаление может вызвать цепочку вращений вплоть до корня).

---

## Код решения

```python
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
        if root is not None and not self.is_valid_avl():
            raise ValueError('Provided root node violates AVL invariants')

    @staticmethod
    def get_height(node: AVLNode | None) -> int:
        return node.height if node is not None else 0

    def get_balance(self, node: AVLNode | None) -> int:
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

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

        x.right = y
        y.left = t2

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

        y.left = x
        x.right = t2

        self._update_height(x)
        self._update_height(y)

        return y

    # 1. Вставка
    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: AVLNode | None, key: int) -> AVLNode:
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Дубликаты игнорируются

        self._update_height(node)
        balance = self.get_balance(node)

        # LL
        if balance > 1 and node.left is not None and key < node.left.key:
            return self.right_rotate(node)

        # RR
        if balance < -1 and node.right is not None and key > node.right.key:
            return self.left_rotate(node)

        # LR
        if balance > 1 and node.left is not None and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RL
        if balance < -1 and node.right is not None and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # 2. Удаление
    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: AVLNode | None, key: int) -> AVLNode | None:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            successor = self._min_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        self._update_height(node)
        balance = self.get_balance(node)

        # LL
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # LR
        if balance > 1 and self.get_balance(node.left) < 0:
            assert node.left is not None
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RR
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # RL
        if balance < -1 and self.get_balance(node.right) > 0:
            assert node.right is not None
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    @staticmethod
    def _min_node(node: AVLNode) -> AVLNode:
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    # 3. Поиск
    def search(self, key: int) -> AVLNode | None:
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
        return self.search(key) is not None

    def inorder(self) -> list[int]:
        result: list[int] = []

        def _traverse(node: AVLNode | None) -> None:
            if node is not None:
                _traverse(node.left)
                result.append(node.key)
                _traverse(node.right)

        _traverse(self.root)
        return result

    def is_valid_avl(self) -> bool:
        keys = self.inorder()
        if keys != sorted(set(keys)):
            return False

        def _check(node: AVLNode | None) -> tuple[bool, int]:
            if node is None:
                return True, 0
            left_ok, lh = _check(node.left)
            right_ok, rh = _check(node.right)
            if not left_ok or not right_ok or abs(lh - rh) > 1:
                return False, 0
            if node.height != 1 + max(lh, rh):
                return False, 0
            return True, 1 + max(lh, rh)

        valid, _ = _check(self.root)
        return valid

    def visualize(self) -> str:
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
```

---

## Оценка сложности

| Операция | Временная сложность (Worst / Avg) | Пространственная сложность (Aux Space) | Причина логарифмической границы |
|:---|:---:|:---:|:---|
| **Поиск (`search`)** | $O(\log N)$ | $O(1)$ | Высота дерева строго ограничена $h \le 1.44 \log_2 N$. Итеративный спуск. |
| **Вставка (`insert`)** | $O(\log N)$ | $O(\log N)$ | Рекурсивный спуск на глубину $h$, затем не более 2 вращений (каждое за $O(1)$). |
| **Удаление (`delete`)** | $O(\log N)$ | $O(\log N)$ | Поиск за $O(h)$, поиск преемника за $O(h)$ и ребалансировка на пути к корню ($O(h)$ вращений по $O(1)$). |

- **Худший случай для обычного BST:** при монотонной вставке ($1, 2, 3, \dots, N$) обычное BST вырождается в список со сложностью операций $O(N)$.
- **В AVL-дереве:** при монотонной вставке $1..100$ высота дерева составляет **всего 7**, гарантируя мгновенный отклик даже на больших объемах данных.

---

## Пошаговая визуализация работы алгоритмов

### Пример 1. Худший случай для наивного BST против триумфа AVL (Вставка отсортированного массива `1..7`)

Классическая и главная слабость обычных двоичных деревьев поиска — вставка отсортированных данных. В обычном BST монотонная последовательность `[1, 2, 3, 4, 5, 6, 7]` вырождается в связный список глубиной 7, превращая поиск в медленный линейный скан $O(N)$.

AVL-дерево в процессе вставки динамически устраняет дисбаланс. Ниже приведена полная последовательность состояний дерева после добавления каждого элемента (корень на каждом шаге: **1, 1, 2, 2, 2, 4, 4**):

#### Шаг 1. Вставка 1
Корень `1`, $h=1$:
```text
1 (h=1)
```

#### Шаг 2. Вставка 2
Добавление в правое поддерево. $BF(1) = 0 - 1 = -1$, баланс в норме. Корень `1`, $h=2$:
```text
1 (h=2)
\-- 2 (h=1)
```

#### Шаг 3. Вставка 3 (Вращение RR вокруг узла 1)
Добавление 3 дает цепочку `1 -> 2 -> 3`.
- $BF(1) = 0 - 2 = -2$, правый ребенок имеет $BF(2) = 0 - 1 = -1 \le 0$ (случай RR).
- Выполняется **малое левое вращение вокруг 1**. Новым корнем становится **2**:
```text
  2 (h=2)
 / \
1   3
```

#### Шаг 4. Вставка 4
Добавление 4 в правое поддерево узла 3:
- $BF(3) = 0 - 1 = -1$, $BF(2) = 1 - 2 = -1$. Вращений не требуется. Корень **2**, $h=3$:
```text
  2 (h=3)
 / \
1   3 (h=2)
     \
      4 (h=1)
```

#### Шаг 5. Вставка 5 (Локальное вращение RR вокруг поддерева 3)
Добавление 5 в правое поддерево 4:
- В узле 3 возникает $BF(3) = 0 - 2 = -2$. Выполняется **малое левое вращение вокруг узла 3** $\to$ поддерево принимает корень 4 с детьми 3 и 5 ($h=2$).
- При подъеме к корню 2: левое поддерево имеет высоту 1, правое (узел 4) — высоту 2. Фактор баланса корня $BF(2) = 1 - 2 = -1 \implies$ **вращения в корне нет, корень остается 2**, $h=3$:
```text
  2 (h=3)
 / \
1   4 (h=2)
   / \
  3   5 (h=1)
```

#### Шаг 6. Вставка 6 (Вращение RR вокруг корня 2)
Добавление 6 в правое поддерево узла 5 ($h=2$ для узла 5, $h=3$ для узла 4):
- В корне 2 возникает критический перевес справа: $BF(2) = 1 - 3 = -2$.
- Правый потомок 4 имеет $BF(4) = 1 - 2 = -1 \le 0$ (случай RR).
- Выполняется **малое левое вращение вокруг корня 2**. Новым корнем дерева становится **4**:
```text
       4 (h=3)
     /         \
  2 (h=2)       5 (h=2)
 /   \           \
1     3           6 (h=1)
```

#### Шаг 7. Вставка 7 (Локальное вращение RR вокруг узла 5)
Добавление 7 в правое поддерево 6:
- В узле 5 возникает $BF(5) = 0 - 2 = -2$. Выполняется **малое левое вращение вокруг узла 5** $\to$ узел 6 становится родителем 5 и 7.
- При подъеме к корню 4: обе ветви имеют высоту 2, $BF(4) = 0$.

#### Итоговое состояние дерева после вставки 1..7:
Вместо вырожденного списка глубиной 7 дерево автоматически трансформировалось в **идеальное полное бинарное дерево минимальной высоты 3**:
```text
               4 (h=3)
             /         \
          2 (h=2)       6 (h=2)
         /       \     /       \
        1         3   5         7
```
```text
4 (h=3)
|-- 2 (h=2)
|   |-- 1 (h=1)
|   \-- 3 (h=1)
\-- 6 (h=2)
    |-- 5 (h=1)
    \-- 7 (h=1)
```
Поиск любого ключа (например, 7) требует **всего 3 сравнения** вместо 7 в обычном BST!

---

### Пример 2. Истинная каскадная ребалансировка при удалении

В отличие от вставки (где балансировка всегда завершается за одно малое или большое вращение), удаление может уменьшить высоту поддерева и **спровоцировать цепочку независимых вращений вверх по дереву вплоть до корня**.

Рассмотрим AVL-дерево из 12 узлов (`[5, 6, 3, 9, 8, 10, 2, 1, 7, 11, 4, 12]`):

```text
               5 (h=5)
             /         \
          2 (h=3)       8 (h=4)
         /   \         /   \
        1     3       6     10 (h=3)
               \       \   /  \
                4       7 9    11 (h=2)
                                 \
                                  12 (h=1)
```

#### Удаление листа 1 (запуск каскада):
1. **Первый поворот (уровень поддерева):**
   - Узел 1 удален. В родительском узле 2 левое поддерево становится пустым ($h=0$), правое (узел 3) имеет высоту 2.
   - $BF(2) = 0 - 2 = -2$ (критический перевес справа).
   - Правый ребенок 3 имеет $BF(3) = 0 - 1 = -1 \le 0$ (случай RR).
   - Выполняется **малое левое вращение вокруг узла 2**: узел 3 становится родителем 2 и 4.
   - **Высота левого поддерева корня падает с 3 до 2.**
2. **Второй поворот (каскадный перенос на корень):**
   - Раскрутка рекурсии поднимается в корень 5.
   - Левое поддерево теперь имеет высоту 2 (узел 3), а правое — высоту 4 (узел 8).
   - $BF(5) = 2 - 4 = -2$ (критический перевес справа распространился на корень!).
   - Правый потомок 8 имеет левую высоту 2 (узел 6) и правую 3 (узел 10), $BF(8) = 2 - 3 = -1 \le 0$ (случай RR).
   - Выполняется **малое левое вращение вокруг корня 5**!
   - Узел 8 становится **новым корнем всего дерева**, узел 5 опускается и становится его левым ребенком.
   - **Высота всего дерева уменьшается с 5 до 4.**

#### Состояние дерева после каскадной ребалансировки:
```text
8 (h=4)
|-- 5 (h=3)
|   |-- 3 (h=2)
|   |   |-- 2 (h=1)
|   |   \-- 4 (h=1)
|   \-- 6 (h=2)
|       |-- None
|       \-- 7 (h=1)
\-- 10 (h=3)
    |-- 9 (h=1)
    \-- 11 (h=2)
        |-- None
        \-- 12 (h=1)
```
Один вызов `delete(1)` спровоцировал каскад из **двух независимых вращений** на разных этажах дерева: сначала левое вращение на узле 2, а затем левое вращение на корне 5.

