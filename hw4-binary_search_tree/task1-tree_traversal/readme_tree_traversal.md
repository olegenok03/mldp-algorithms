# Бинарное дерево поиска: вставка и обходы

## 1. Метод вставки узла (`insert`)

Бинарное дерево поиска (BST) обладает свойством: для любого узла с ключом $K$ все ключи в левом поддереве строго меньше $K$, а в правом — строго больше $K$.

Метод `insert` реализован **итеративно**, без рекурсии, что гарантирует работу за $O(1)$ дополнительной памяти и отсутствие риска переполнения системного стека (`RecursionError`).

### Код метода

```python
def insert(self, key: int) -> None:
    if self.root is None:
        self.root = TreeNode(key)
        return

    curr = self.root
    while True:
        if key < curr.key:
            if curr.left is None:
                curr.left = TreeNode(key)
                return
            curr = curr.left
        elif key > curr.key:
            if curr.right is None:
                curr.right = TreeNode(key)
                return
            curr = curr.right
        else:
            # Ключ уже присутствует в BST (дубликаты игнорируются)
            return
```

### Логика работы
1. **Пустое дерево:** Если корень отсутствует (`self.root is None`), создаём `TreeNode(key)` и делаем его корнем дерева.
2. **Поиск позиции:** Инициализируем указатель `curr = self.root` и в цикле спускаемся по дереву:
   - Если вставляемый `key < curr.key`, то согласно инварианту BST новый узел должен находиться в левом поддереве:
     - Если `curr.left is None`, мы нашли подходящее место — создаём новый узел `curr.left = TreeNode(key)` и завершаем выполнение.
     - Иначе перемещаем указатель влево: `curr = curr.left`.
   - Если `key > curr.key`, новый узел должен находиться в правом поддереве:
     - Если `curr.right is None`, создаём новый узел `curr.right = TreeNode(key)` и завершаем выполнение.
     - Иначе перемещаем указатель вправо: `curr = curr.right`.
   - Если `key == curr.key`, ключ уже присутствует в дереве. По соглашению множеств дубликаты повторно не вставляются.

### Оценка сложности
- **Временная сложность:** $O(H)$, где $H$ — высота дерева ($O(\log N)$ в сбалансированном дереве, $O(N)$ в худшем вырожденном случае).
- **Пространственная сложность:** $O(1)$ дополнительной памяти (алгоритм итеративный, используются только локальные ссылки).

### Визуализация вставки

Рассмотрим вставку ключа `5` в существующее BST:

```text
    Дерево ДО вставки ключа 5:            Дерево ПОСЛЕ вставки ключа 5:

               4                                        4
             /   \                                    /   \
            2     6                                  2     6
           / \                                      / \   /
          1   3                                    1   3 5
```

### Трассировка вызова `insert(5)`

| Шаг | Текущий узел `curr` | Сравнение ключей | Ветка `if/elif` | Наличие потомка | Выполняемое действие |
|:---:|:-------------------:|:----------------:|:---------------:|:---------------:|---|
| 1   | `Node(4)`           | `5 > 4`          | `key > curr.key`| `curr.right` существует (`Node(6)`) | Переход в правое поддерево: `curr = curr.right` |
| 2   | `Node(6)`           | `5 < 6`          | `key < curr.key`| `curr.left is None` | Найдено пустое место. Создание узла: `curr.left = TreeNode(5)`. Выход (`return`) |

---

## 2. Методы обхода дерева (Traversals)

В бинарном дереве обходы определяют порядок посещения узлов. Традиционные прямые (left-to-right) обходы посещают левое поддерево раньше правого, а **обратные (reverse / right-to-left)** зеркально меняют порядок детей (правое поддерево раньше левого):

1. **Pre-order (прямой):** `Корень` $\to$ `Левый` $\to$ `Правый` ($N \to L \to R$)
2. **Reverse pre-order (обратный прямой):** `Корень` $\to$ `Правый` $\to$ `Левый` ($N \to R \to L$)
3. **In-order (симметричный):** `Левый` $\to$ `Корень` $\to$ `Правый` ($L \to N \to R$)
4. **Reverse in-order (обратный симметричный):** `Правый` $\to$ `Корень` $\to$ `Левый` ($R \to N \to L$)
5. **Post-order (концевой):** `Левый` $\to$ `Правый` $\to$ `Корень` ($L \to R \to N$)
6. **Reverse post-order (обратный концевой):** `Правый` $\to$ `Левый` $\to$ `Корень` ($R \to L \to N$)

Все 6 методов реализованы **итеративно** с использованием единого шаблона — указателя текущего узла `curr` и явного стека `tree_stack`.

> **Симметрия reverse-обходов:**  
> Каждый reverse-метод получается из соответствующего прямого обхода зеркальной заменой всех обращений к потомкам: `left` меняется на `right`, а `right` на `left`.

---

### 2.1. Pre-order и Reverse Pre-order

Узел записывается в результат **до** спуска в поддеревья.

```python
def get_preorder(self) -> list[int]:
    res = []
    tree_stack = []
    curr = self.root

    while curr is not None or tree_stack:
        if curr is not None:
            res.append(curr.key)
            tree_stack.append(curr)
            curr = curr.left
        else:
            curr = tree_stack.pop()
            curr = curr.right

    return res

def get_reverse_preorder(self) -> list[int]:
    res = []
    tree_stack = []
    curr = self.root

    while curr is not None or tree_stack:
        if curr is not None:
            res.append(curr.key)
            tree_stack.append(curr)
            curr = curr.right
        else:
            curr = tree_stack.pop()
            curr = curr.left

    return res
```

---

### 2.2. In-order и Reverse In-order

Узел записывается в результат **между** обходами двух своих поддеревьев (в момент снятия со стека).  
- Для BST обычный in-order даёт ключи по **возрастанию** ($1, 2, 3, \dots$).
- Reverse in-order даёт ключи строго по **убыванию** ($\dots, 3, 2, 1$).

```python
def get_inorder(self) -> list[int]:
    res = []
    tree_stack = []
    curr = self.root

    while curr is not None or tree_stack:
        if curr is not None:
            tree_stack.append(curr)
            curr = curr.left
        else:
            curr = tree_stack.pop()
            res.append(curr.key)
            curr = curr.right

    return res

def get_reverse_inorder(self) -> list[int]:
    res = []
    tree_stack = []
    curr = self.root

    while curr is not None or tree_stack:
        if curr is not None:
            tree_stack.append(curr)
            curr = curr.right
        else:
            curr = tree_stack.pop()
            res.append(curr.key)
            curr = curr.left

    return res
```

---

### 2.3. Post-order (концевой) и Reverse Post-order (обратный концевой)

Узел записывается в результат **после** полного завершения обхода обоих поддеревьев. Для предотвращения преждевременного извлечения родителя со стека используется переменная `last_visited`.

```python
def get_postorder(self) -> list[int]:
    res = []
    tree_stack = []
    curr = self.root
    last_visited = None

    while curr is not None or tree_stack:
        if curr is not None:
            tree_stack.append(curr)
            curr = curr.left
        else:
            peek_node = tree_stack[-1]
            if peek_node.right is not None and last_visited != peek_node.right:
                curr = peek_node.right
            else:
                res.append(peek_node.key)
                last_visited = tree_stack.pop()

    return res

def get_reverse_postorder(self) -> list[int]:
    res = []
    tree_stack = []
    curr = self.root
    last_visited = None

    while curr is not None or tree_stack:
        if curr is not None:
            tree_stack.append(curr)
            curr = curr.right
        else:
            peek_node = tree_stack[-1]
            if peek_node.left is not None and last_visited != peek_node.left:
                curr = peek_node.left
            else:
                res.append(peek_node.key)
                last_visited = tree_stack.pop()

    return res
```

### Оценка сложности всех 6 методов
- **Время:** $O(N)$, где $N$ — число узлов в дереве. Каждый узел попадает в стек и извлекается ровно один раз.
- **Память:** $O(H)$, где $H$ — высота дерева ($O(\log N)$ в сбалансированном дереве, $O(N)$ в худшем вырожденном случае). Стек вызовов Python не расходуется, что исключает `RecursionError` даже на $10^4$ узлах.

---

## 3. Визуализация работы обходов

Рассмотрим работу всех методов на примере бинарного дерева поиска:

```text
         4
       /   \
      2     6
     / \   /
    1   3 5
```

Итоговые порядки обхода для данного дерева:
- **Pre-order:** `[4, 2, 1, 3, 6, 5]`
- **Reverse pre-order:** `[4, 6, 5, 2, 3, 1]`
- **In-order:** `[1, 2, 3, 4, 5, 6]` (по возрастанию)
- **Reverse in-order:** `[6, 5, 4, 3, 2, 1]` (по убыванию)
- **Post-order (концевой):** `[1, 3, 2, 5, 6, 4]`
- **Reverse post-order (обратный концевой):** `[5, 6, 3, 1, 2, 4]`

---

### Таблица 1. Пошаговое выполнение `get_preorder` ($N \to L \to R$)

| Шаг | `curr` | `tree_stack` (ключи) | `res` | Выполняемое действие / Событие |
|:---:|:------:|:--------------------:|:-----:|---|
| 1   | `Node(4)` | `[]`            | `[]`  | Спуск в 4. Запись `4` в `res`, push 4 в стек, `curr = 4.left` |
| 2   | `Node(2)` | `[4]`           | `[4]` | Спуск в 2. Запись `2` в `res`, push 2 в стек, `curr = 2.left` |
| 3   | `Node(1)` | `[4, 2]`        | `[4, 2]` | Спуск в 1. Запись `1` в `res`, push 1 в стек, `curr = 1.left` |
| 4   | `None`    | `[4, 2, 1]`     | `[4, 2, 1]` | Тупик слева. `pop()` ➔ 1. `curr = 1.right` (`None`) |
| 5   | `None`    | `[4, 2]`        | `[4, 2, 1]` | Тупик. `pop()` ➔ 2. `curr = 2.right` (`Node(3)`) |
| 6   | `Node(3)` | `[4]`           | `[4, 2, 1, 3]` | Спуск в 3. Запись `3` в `res`, push 3 в стек, `curr = 3.left` |
| 7   | `None`    | `[4, 3]`        | `[4, 2, 1, 3]` | Тупик слева. `pop()` ➔ 3. `curr = 3.right` (`None`) |
| 8   | `None`    | `[4]`           | `[4, 2, 1, 3]` | Тупик. `pop()` ➔ 4. `curr = 4.right` (`Node(6)`) |
| 9   | `Node(6)` | `[]`            | `[4, 2, 1, 3, 6]` | Спуск в 6. Запись `6` в `res`, push 6 в стек, `curr = 6.left` |
| 10  | `Node(5)` | `[6]`           | `[4, 2, 1, 3, 6, 5]` | Спуск в 5. Запись `5` в `res`, push 5 в стек, `curr = 5.left` |
| 11  | `None`    | `[6, 5]`        | `[4, 2, 1, 3, 6, 5]` | Тупик слева. `pop()` ➔ 5. `curr = 5.right` (`None`) |
| 12  | `None`    | `[6]`           | `[4, 2, 1, 3, 6, 5]` | Тупик. `pop()` ➔ 6. `curr = 6.right` (`None`) |
| 13  | `None`    | `[]`            | `[4, 2, 1, 3, 6, 5]` | Стек пуст и `curr is None`. Завершение работы |

---

### Таблица 2. Пошаговое выполнение `get_reverse_preorder` ($N \to R \to L$)

| Шаг | `curr` | `tree_stack` (ключи) | `res` | Выполняемое действие / Событие |
|:---:|:------:|:--------------------:|:-----:|---|
| 1   | `Node(4)` | `[]`            | `[]`  | Спуск в 4. Запись `4` в `res`, push 4 в стек, `curr = 4.right` |
| 2   | `Node(6)` | `[4]`           | `[4]` | Спуск в 6. Запись `6` в `res`, push 6 в стек, `curr = 6.right` (`None`) |
| 3   | `None`    | `[4, 6]`        | `[4, 6]` | Тупик справа. `pop()` ➔ 6. `curr = 6.left` (`Node(5)`) |
| 4   | `Node(5)` | `[4]`           | `[4, 6, 5]` | Спуск в 5. Запись `5` в `res`, push 5 в стек, `curr = 5.right` (`None`) |
| 5   | `None`    | `[4, 5]`        | `[4, 6, 5]` | Тупик справа. `pop()` ➔ 5. `curr = 5.left` (`None`) |
| 6   | `None`    | `[4]`           | `[4, 6, 5]` | Тупик. `pop()` ➔ 4. `curr = 4.left` (`Node(2)`) |
| 7   | `Node(2)` | `[]`            | `[4, 6, 5, 2]` | Спуск в 2. Запись `2` в `res`, push 2 в стек, `curr = 2.right` (`Node(3)`) |
| 8   | `Node(3)` | `[2]`           | `[4, 6, 5, 2, 3]` | Спуск в 3. Запись `3` в `res`, push 3 в стек, `curr = 3.right` (`None`) |
| 9   | `None`    | `[2, 3]`        | `[4, 6, 5, 2, 3]` | Тупик справа. `pop()` ➔ 3. `curr = 3.left` (`None`) |
| 10  | `None`    | `[2]`           | `[4, 6, 5, 2, 3]` | Тупик. `pop()` ➔ 2. `curr = 2.left` (`Node(1)`) |
| 11  | `Node(1)` | `[]`            | `[4, 6, 5, 2, 3, 1]` | Спуск в 1. Запись `1` в `res`, push 1 в стек, `curr = 1.right` (`None`) |
| 12  | `None`    | `[1]`           | `[4, 6, 5, 2, 3, 1]` | Тупик справа. `pop()` ➔ 1. `curr = 1.left` (`None`) |
| 13  | `None`    | `[]`            | `[4, 6, 5, 2, 3, 1]` | Стек пуст и `curr is None`. Завершение работы |

---

### Таблица 3. Пошаговое выполнение `get_inorder` ($L \to N \to R$)

| Шаг | `curr` | `tree_stack` (ключи) | `res` | Выполняемое действие / Событие |
|:---:|:------:|:--------------------:|:-----:|---|
| 1   | `Node(4)` | `[]`            | `[]`  | Push 4 в стек, спуск влево: `curr = 4.left` |
| 2   | `Node(2)` | `[4]`           | `[]`  | Push 2 в стек, спуск влево: `curr = 2.left` |
| 3   | `Node(1)` | `[4, 2]`        | `[]`  | Push 1 в стек, спуск влево: `curr = 1.left` |
| 4   | `None`    | `[4, 2, 1]`     | `[]`  | Тупик слева. `pop()` ➔ 1. Запись `1` в `res`. `curr = 1.right` (`None`) |
| 5   | `None`    | `[4, 2]`        | `[1]` | Тупик. `pop()` ➔ 2. Запись `2` в `res`. `curr = 2.right` (`Node(3)`) |
| 6   | `Node(3)` | `[4]`           | `[1, 2]` | Push 3 в стек, спуск влево: `curr = 3.left` |
| 7   | `None`    | `[4, 3]`        | `[1, 2]` | Тупик слева. `pop()` ➔ 3. Запись `3` в `res`. `curr = 3.right` (`None`) |
| 8   | `None`    | `[4]`           | `[1, 2, 3]` | Тупик. `pop()` ➔ 4. Запись `4` в `res`. `curr = 4.right` (`Node(6)`) |
| 9   | `Node(6)` | `[]`            | `[1, 2, 3, 4]` | Push 6 в стек, спуск влево: `curr = 6.left` |
| 10  | `Node(5)` | `[6]`           | `[1, 2, 3, 4]` | Push 5 в стек, спуск влево: `curr = 5.left` |
| 11  | `None`    | `[6, 5]`        | `[1, 2, 3, 4]` | Тупик слева. `pop()` ➔ 5. Запись `5` в `res`. `curr = 5.right` (`None`) |
| 12  | `None`    | `[6]`           | `[1, 2, 3, 4, 5]` | Тупик. `pop()` ➔ 6. Запись `6` в `res`. `curr = 6.right` (`None`) |
| 13  | `None`    | `[]`            | `[1, 2, 3, 4, 5, 6]` | Стек пуст и `curr is None`. Завершение работы |

---

### Таблица 4. Пошаговое выполнение `get_reverse_inorder` ($R \to N \to L$)

| Шаг | `curr` | `tree_stack` (ключи) | `res` | Выполняемое действие / Событие |
|:---:|:------:|:--------------------:|:-----:|---|
| 1   | `Node(4)` | `[]`            | `[]`  | Push 4 в стек, спуск вправо: `curr = 4.right` |
| 2   | `Node(6)` | `[4]`           | `[]`  | Push 6 в стек, спуск вправо: `curr = 6.right` (`None`) |
| 3   | `None`    | `[4, 6]`        | `[]`  | Тупик справа. `pop()` ➔ 6. Запись `6` в `res`. `curr = 6.left` (`Node(5)`) |
| 4   | `Node(5)` | `[4]`           | `[6]` | Push 5 в стек, спуск вправо: `curr = 5.right` (`None`) |
| 5   | `None`    | `[4, 5]`        | `[6]` | Тупик справа. `pop()` ➔ 5. Запись `5` в `res`. `curr = 5.left` (`None`) |
| 6   | `None`    | `[4]`           | `[6, 5]` | Тупик. `pop()` ➔ 4. Запись `4` в `res`. `curr = 4.left` (`Node(2)`) |
| 7   | `Node(2)` | `[]`            | `[6, 5, 4]` | Push 2 в стек, спуск вправо: `curr = 2.right` (`Node(3)`) |
| 8   | `Node(3)` | `[2]`           | `[6, 5, 4]` | Push 3 в стек, спуск вправо: `curr = 3.right` (`None`) |
| 9   | `None`    | `[2, 3]`        | `[6, 5, 4]` | Тупик справа. `pop()` ➔ 3. Запись `3` в `res`. `curr = 3.left` (`None`) |
| 10  | `None`    | `[2]`           | `[6, 5, 4, 3]` | Тупик. `pop()` ➔ 2. Запись `2` в `res`. `curr = 2.left` (`Node(1)`) |
| 11  | `Node(1)` | `[]`            | `[6, 5, 4, 3, 2]` | Push 1 в стек, спуск вправо: `curr = 1.right` (`None`) |
| 12  | `None`    | `[1]`           | `[6, 5, 4, 3, 2]` | Тупик справа. `pop()` ➔ 1. Запись `1` в `res`. `curr = 1.left` (`None`) |
| 13  | `None`    | `[]`            | `[6, 5, 4, 3, 2, 1]` | Стек пуст и `curr is None`. Завершение работы |

---

### Таблица 5. Пошаговое выполнение `get_postorder` (концевой, $L \to R \to N$)

| Шаг | `curr` | `tree_stack` (ключи) | `last_visited` | `res` | Выполняемое действие / Событие |
|:---:|:------:|:--------------------:|:--------------:|:-----:|---|
| 1   | `Node(4)` | `[]`            | `None`         | `[]`  | Push 4 в стек, `curr = 4.left` |
| 2   | `Node(2)` | `[4]`           | `None`         | `[]`  | Push 2 в стек, `curr = 2.left` |
| 3   | `Node(1)` | `[4, 2]`        | `None`         | `[]`  | Push 1 в стек, `curr = 1.left` |
| 4   | `None`    | `[4, 2, 1]`     | `None`         | `[]`  | Смотрим вершину (1): `1.right is None`. `pop()` ➔ 1, `res.append(1)`, `last_visited = 1` |
| 5   | `None`    | `[4, 2]`        | `Node(1)`      | `[1]` | Смотрим вершину (2): `2.right` (3) $\neq$ `last_visited`. Переход: `curr = Node(3)` |
| 6   | `Node(3)` | `[4, 2]`        | `Node(1)`      | `[1]` | Push 3 в стек, `curr = 3.left` (`None`) |
| 7   | `None`    | `[4, 2, 3]`     | `Node(1)`      | `[1]` | Смотрим вершину (3): `3.right is None`. `pop()` ➔ 3, `res.append(3)`, `last_visited = 3` |
| 8   | `None`    | `[4, 2]`        | `Node(3)`      | `[1, 3]` | Смотрим вершину (2): `2.right` (3) $==$ `last_visited`. `pop()` ➔ 2, `res.append(2)`, `last_visited = 2` |
| 9   | `None`    | `[4]`           | `Node(2)`      | `[1, 3, 2]` | Смотрим вершину (4): `4.right` (6) $\neq$ `last_visited`. Переход: `curr = Node(6)` |
| 10  | `Node(6)` | `[4]`           | `Node(2)`      | `[1, 3, 2]` | Push 6 в стек, `curr = 6.left` (`Node(5)`) |
| 11  | `Node(5)` | `[4, 6]`        | `Node(2)`      | `[1, 3, 2]` | Push 5 в стек, `curr = 5.left` (`None`) |
| 12  | `None`    | `[4, 6, 5]`     | `Node(2)`      | `[1, 3, 2]` | Смотрим вершину (5): `5.right is None`. `pop()` ➔ 5, `res.append(5)`, `last_visited = 5` |
| 13  | `None`    | `[4, 6]`        | `Node(5)`      | `[1, 3, 2, 5]` | Смотрим вершину (6): `6.right is None`. `pop()` ➔ 6, `res.append(6)`, `last_visited = 6` |
| 14  | `None`    | `[4]`           | `Node(6)`      | `[1, 3, 2, 5, 6]` | Смотрим вершину (4): `4.right` (6) $==$ `last_visited`. `pop()` ➔ 4, `res.append(4)`, `last_visited = 4` |
| 15  | `None`    | `[]`            | `Node(4)`      | `[1, 3, 2, 5, 6, 4]` | Стек пуст и `curr is None`. Завершение работы |

---

### Таблица 6. Пошаговое выполнение `get_reverse_postorder` (обратный концевой, $R \to L \to N$)

| Шаг | `curr` | `tree_stack` (ключи) | `last_visited` | `res` | Выполняемое действие / Событие |
|:---:|:------:|:--------------------:|:--------------:|:-----:|---|
| 1   | `Node(4)` | `[]`            | `None`         | `[]`  | Push 4 в стек, `curr = 4.right` |
| 2   | `Node(6)` | `[4]`           | `None`         | `[]`  | Push 6 в стек, `curr = 6.right` (`None`) |
| 3   | `None`    | `[4, 6]`        | `None`         | `[]`  | Смотрим вершину (6): `6.left` (5) $\neq$ `last_visited`. Переход: `curr = Node(5)` |
| 4   | `Node(5)` | `[4, 6]`        | `None`         | `[]`  | Push 5 в стек, `curr = 5.right` (`None`) |
| 5   | `None`    | `[4, 6, 5]`     | `None`         | `[]`  | Смотрим вершину (5): `5.left is None`. `pop()` ➔ 5, `res.append(5)`, `last_visited = 5` |
| 6   | `None`    | `[4, 6]`        | `Node(5)`      | `[5]` | Смотрим вершину (6): `6.left` (5) $==$ `last_visited`. `pop()` ➔ 6, `res.append(6)`, `last_visited = 6` |
| 7   | `None`    | `[4]`           | `Node(6)`      | `[5, 6]` | Смотрим вершину (4): `4.left` (2) $\neq$ `last_visited`. Переход: `curr = Node(2)` |
| 8   | `Node(2)` | `[4]`           | `Node(6)`      | `[5, 6]` | Push 2 в стек, `curr = 2.right` (`Node(3)`) |
| 9   | `Node(3)` | `[4, 2]`        | `Node(6)`      | `[5, 6]` | Push 3 в стек, `curr = 3.right` (`None`) |
| 10  | `None`    | `[4, 2, 3]`     | `Node(6)`      | `[5, 6]` | Смотрим вершину (3): `3.left is None`. `pop()` ➔ 3, `res.append(3)`, `last_visited = 3` |
| 11  | `None`    | `[4, 2]`        | `Node(3)`      | `[5, 6, 3]` | Смотрим вершину (2): `2.left` (1) $\neq$ `last_visited`. Переход: `curr = Node(1)` |
| 12  | `Node(1)` | `[4, 2]`        | `Node(3)`      | `[5, 6, 3]` | Push 1 в стек, `curr = 1.right` (`None`) |
| 13  | `None`    | `[4, 2, 1]`     | `Node(3)`      | `[5, 6, 3]` | Смотрим вершину (1): `1.left is None`. `pop()` ➔ 1, `res.append(1)`, `last_visited = 1` |
| 14  | `None`    | `[4, 2]`        | `Node(1)`      | `[5, 6, 3, 1]` | Смотрим вершину (2): `2.left` (1) $==$ `last_visited`. `pop()` ➔ 2, `res.append(2)`, `last_visited = 2` |
| 15  | `None`    | `[4]`           | `Node(2)`      | `[5, 6, 3, 1, 2]` | Смотрим вершину (4): `4.left` (2) $==$ `last_visited`. `pop()` ➔ 4, `res.append(4)`, `last_visited = 4` |
| 16  | `None`    | `[]`            | `Node(4)`      | `[5, 6, 3, 1, 2, 4]` | Стек пуст и `curr is None`. Завершение работы |
