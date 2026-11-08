# Задание 2. Permutations

Поскольку в исходной постановке несколько критически важных для трактовки задачи ограничений было опущено, условие было дополнено в соответствии с формулировкой с leetcode (по-видимому, условие брали оттуда).  

## Постановка задачи

На вход дан массив целых чисел `arr` (все элементы уникальны). Необходимо вернуть все возможные перестановки элементов в любом порядке.

**Примеры:**
- Вход: `nums = [1, 2, 3]` $\to$ Выход: `[[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]` (всего $3! = 6$ перестановок)
- Вход: `nums = [0, 1]` $\to$ Выход: `[[0,1], [1,0]]` (всего $2! = 2$ перестановки)
- Вход: `nums = [1]` $\to$ Выход: `[[1]]` (всего $1! = 1$ перестановка)

**Ограничения:**
- $1 \le \text{len}(nums) \le 6$;
- $-10 \le nums[i] \le 10$;
- Все элементы уникальны.

**Обязательное условие учебного задания:**
> В реализации предусмотрена визуализация стека вызовов с помощью декоратора `@tracer` из первой задачи.

В решении представлены два дополняющих друг друга подхода:
1. **Вариант 1 (`get_permutations`):** Классический рекурсивный поиск с возвратом (Backtracking) с булевой маской использованных элементов и поэлементным накоплением текущей перестановки.
2. **Вариант 2 (`get_permutations_inplace`):** Оптимизированный In-Place алгоритм на основе обмена элементов (`swap`), формирующий перестановки непосредственно внутри исходного массива без дополнительных структур данных и с гарантированным возвратом массива в исходное состояние.

---

## Вариант 1. Рекурсивный Backtracking с булевой маской

### Идея алгоритма

1. **Единый аккумулятор результата (`res = []`):**  
   Вместо неэффективного возврата промежуточных списков с каждого этажа рекурсии и их склеивания (`res += sub_perms`), результат накапливается в одном общем списке на уровне внешней функции.
2. **Контроль занятости элементов (`is_used: list[bool]`):**  
   Массив булевых флагов размера $N$ позволяет за $O(1)$ проверять, добавлен ли уже элемент с индексом $i$ в текущую префиксную последовательность.
3. **Прямой ход (спуск):**  
   Перебираем элементы `arr`. Если элемент свободен (`not is_used[i]`), помечаем его занятым (`is_used[i] = True`), добавляем в формируемую перестановку (`current_perm.append(num)`) и рекурсивно вызываем `backtrack()`.
4. **Базовый случай:**  
   Когда длина текущей перестановки достигает $N$ (`len(current_perm) == len(arr)`), готовая комбинация копируется в ответ: `res.append(current_perm.copy())`. Копирование выполняется ровно $N!$ раз — только в момент готовности очередной перестановки.
5. **Обратный ход (backtrack / откат):**  
   После возврата из рекурсивного вызова снимаем флаг (`is_used[i] = False`) и удаляем последний добавленный элемент (`current_perm.pop()`), восстанавливая исходное состояние для следующей итерации.

### Код решения (Вариант 1)

```python
@tracer
def get_permutations(arr: list[int]) -> list[list[int]]:
    res = []
    is_used = [False] * len(arr)
    current_perm = []

    @tracer
    def backtrack() -> None:
        if len(current_perm) == len(arr):
            res.append(current_perm.copy())
            return

        for i, num in enumerate(arr):
            if is_used[i]:
                continue

            is_used[i] = True
            current_perm.append(num)

            backtrack()

            current_perm.pop()
            is_used[i] = False

    backtrack()
    return res
```

### Оценка сложности (Вариант 1)

- **Временная сложность (Time Complexity):**
  - Дерево рекурсии содержит $N!$ листьев (терминальных состояний). Суммарное количество всех узлов в дереве рекурсии составляет $\sum_{k=0}^{N} \frac{N!}{(N-k)!} < e \cdot N! = O(N!)$.
  - В каждом внутреннем узле выполняется цикл из $N$ итераций с $O(1)$ проверками флага.
  - В каждом листе ($N!$ раз) выполняется копирование списка длины $N$ за $O(N)$.
  - **Итоговая сложность по времени:** $O(N \cdot N!)$. Для максимального $N = 6$: $6 \cdot 720 = 4320$ операций (выполняется за доли миллисекунды).

- **Пространственная сложность (Space Complexity):**
  - Стек вызовов рекурсии достигает максимальной глубины $N$, требуя $O(N)$ памяти.
  - Вспомогательные структуры: булева маска `is_used` размера $N$ и список `current_perm` размера $\le N$ занимают $O(N)$ памяти.
  - Результирующий список `res` содержит $N!$ перестановок по $N$ чисел, занимая $O(N \cdot N!)$ памяти (память под требуемый условием ответ).
  - **Вспомогательная память (Auxiliary Space, без ответа):** $O(N)$.

### Визуализация и трассировка (`@tracer`)

Рассмотрим нетривиальный пример $N = 3$ (`[1, 2, 3]`), на котором полностью раскрывается ветвящаяся структура пространства поиска ($3! = 6$ терминальных листьев на глубине 3). 

В трассировке отчетливо видно, как алгоритм фиксирует в корне первый элемент (`1`, затем `2`, затем `3`), и внутри каждой из трех главных ветвей исследует поддерево из $2! = 2$ перестановок:

```text
"get_permutations" call with args ([1, 2, 3],) and kwargs {}.
    "backtrack" call with args () and kwargs {}.
        "backtrack" call with args () and kwargs {}.
            "backtrack" call with args () and kwargs {}.
                "backtrack" call with args () and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
            "backtrack" call with args () and kwargs {}.
                "backtrack" call with args () and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
        "backtrack" terminated.
        "backtrack" call with args () and kwargs {}.
            "backtrack" call with args () and kwargs {}.
                "backtrack" call with args () and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
            "backtrack" call with args () and kwargs {}.
                "backtrack" call with args () and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
        "backtrack" terminated.
        "backtrack" call with args () and kwargs {}.
            "backtrack" call with args () and kwargs {}.
                "backtrack" call with args () and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
            "backtrack" call with args () and kwargs {}.
                "backtrack" call with args () and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
        "backtrack" terminated.
    "backtrack" terminated.
"get_permutations" terminated. Returned value: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]] (of type <class 'list'>).
```

---

## Вариант 2. In-Place Swapping (Перестановки на месте с обменом элементов)

### Идея алгоритма

Алгоритм устраняет необходимость в булевой маске `is_used` и отдельном буфере `current_perm`, формируя перестановки непосредственно внутри переданного массива `arr`:

1. **Разделение массива на две зоны по указателю `first`:**
   - Префикс `arr[0 : first]` — уже зафиксированная часть текущей перестановки.
   - Суффикс `arr[first : len(arr)]` — кандидаты на позицию с индексом `first`.
2. **Цикл только по доступным кандидатам:**  
   В отличие от Варианта 1, цикл `for i in range(first, len(arr))` бежит **только по оставшейся части массива**, уменьшая число итераций на каждом шаге спуска ($N, N-1, \dots, 1$).
3. **Прямой ход (swap):**  
   Меняем местами текущий элемент с кандидатом: `arr[first], arr[i] = arr[i], arr[first]`. Теперь кандидат зафиксирован на позиции `first`. Рекурсивно вызываем `backtrack(first + 1)` для суффикса.
4. **Базовый случай:**  
   Когда `first == len(arr)`, весь массив представляет собой готовую перестановку. Добавляем ее копию: `res.append(arr[:])`.
5. **Обратный ход (backtrack / un-swap):**  
   Снова выполняем тот же обмен: `arr[first], arr[i] = arr[i], arr[first]`. Это возвращает массив в состояние до вызова.
6. **Гарантия сохранности исходных данных:**  
   Поскольку каждый `swap` строго парно компенсируется обратным `swap` при раскрутке стека, после полного завершения работы функции массив `arr` **гарантированно возвращается в исходное состояние**.

### Код решения (Вариант 2)

```python
@tracer
def get_permutations_inplace(arr: list[int]) -> list[list[int]]:
    res = []

    @tracer
    def backtrack(first: int = 0) -> None:
        if first == len(arr):
            res.append(arr[:])
            return

        for i in range(first, len(arr)):
            arr[first], arr[i] = arr[i], arr[first]

            backtrack(first + 1)

            arr[first], arr[i] = arr[i], arr[first]

    backtrack()
    return res
```

### Оценка сложности (Вариант 2)

- **Временная сложность (Time Complexity):**
  - На каждом уровне рекурсии `first` цикл делает ровно $N - first$ итераций.
  - Обмен двух элементов в списке Python выполняется за $O(1)$.
  - В базовом случае выполняется срез `arr[:]` за $O(N)$ ровно $N!$ раз.
  - **Итоговая сложность по времени:** $O(N \cdot N!)$. Асимптотика совпадает с Вариантом 1, однако благодаря отсутствию холостых итераций по занятым элементам скрытая константа времени меньше.

- **Пространственная сложность (Space Complexity):**
  - **Не выделяется память под маски и буферы:** отслеживание состояния и сборка перестановки производятся прямо в исходном массиве `arr`.
  - Память расходуется только на системный стек вызовов глубиной $N$.
  - **Вспомогательная память (Auxiliary Space, без ответа):** $O(N)$ (исключительно стек рекурсии), чистая дополнительная память под структуры данных — $O(1)$.

### Визуализация и трассировка (`@tracer`)

Благодаря тому, что в `backtrack(first)` передается аргумент `first`, трассировщик на нетривиальном примере `[1, 2, 3]` наглядно отражает продвижение границы зафиксированного префикса (`first=0 -> 1 -> 2 -> 3`):

```text
"get_permutations_inplace" call with args ([1, 2, 3],) and kwargs {}.
    "backtrack" call with args () and kwargs {}.
        "backtrack" call with args (1,) and kwargs {}.
            "backtrack" call with args (2,) and kwargs {}.
                "backtrack" call with args (3,) and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
            "backtrack" call with args (2,) and kwargs {}.
                "backtrack" call with args (3,) and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
        "backtrack" terminated.
        "backtrack" call with args (1,) and kwargs {}.
            "backtrack" call with args (2,) and kwargs {}.
                "backtrack" call with args (3,) and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
            "backtrack" call with args (2,) and kwargs {}.
                "backtrack" call with args (3,) and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
        "backtrack" terminated.
        "backtrack" call with args (1,) and kwargs {}.
            "backtrack" call with args (2,) and kwargs {}.
                "backtrack" call with args (3,) and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
            "backtrack" call with args (2,) and kwargs {}.
                "backtrack" call with args (3,) and kwargs {}.
                "backtrack" terminated.
            "backtrack" terminated.
        "backtrack" terminated.
    "backtrack" terminated.
"get_permutations_inplace" terminated. Returned value: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]] (of type <class 'list'>).
```

---

## Сравнительный анализ вариантов

| Критерий | Вариант 1 (`get_permutations`) | Вариант 2 (`get_permutations_inplace`) |
|:---|:---:|:---:|
| **Принцип работы** | Сборка перестановки в буфере `current_perm` | Перестановка элементов на месте через `swap` |
| **Временная сложность** | $O(N \cdot N!)$ | $O(N \cdot N!)$ (меньшая константа) |
| **Вспомогательная память (Aux Space)** | $O(N)$ (стек + `is_used` + `current_perm`) | $O(N)$ (только стек вызовов) |
| **Дополнительные структуры данных** | Список `list[bool]` и `list[int]` | Отсутствуют ($O(1)$) |
| **Итерации цикла во внутреннем узле** | Всегда $N$ итераций (с проверкой флага) | Строго $N - first$ итераций (только кандидаты) |
| **Порядок генерации** | Лексикографический (при отсортированном входе) | Комбинаторный порядок дерева обменов |
| **Сохранность входного массива** | Массив не модифицируется | Модифицируется в процессе, но гарантированно возвращается в исходное состояние |

Оба решения полностью удовлетворяют ограничениям задачи и демонстрируют канонические приемы проектирования рекурсивных алгоритмов поиска с возвратом (Backtracking).
