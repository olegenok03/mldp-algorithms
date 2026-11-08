# Задание 1. Tracer

## Описание решения

В задаче требуется реализовать декоратор для визуализации стека вызовов рекурсивных функций.

### Трактовка условия и постановка задачи

> **Важное замечание о трактовке условия:**
> Условие про отступ было трактовано, как требование к форматированию не только служебных системных сообщений декоратора (`call` / `terminated`), но и **любого внутреннего системного вывода (`print()`, `sys.stdout.write()`, `sys.stderr.write()`)**, выполняемого внутри декорируемой функции и её вложенных вызовов.

> **Архитектурный выбор:**
> Была решена более общая инженерная задача. Вариант с рекурсией и многократным созданием экземпляров `IndentedStream` был отклонен в пользу мутации единственного экземпляра в связи с:
> 1. **Избыточными накладными расходами и риском `RecursionError` внутри потока вывода:** при рекурсивном создании оберток вида $\text{IndentedStream}_N \to \dots \to \text{sys.stdout}$ каждый вывод строки порождал цепочку вызовов глубиной $N$. Это приводило к квадратичной вычислительной сложности $O(N^2)$ при обработке текста и грозило аварийным переполнением стека вызовов Python внутри метода `write()` при умеренно глубокой рекурсии.
> 2. **Рассинхронизацией флага начала строки `_at_line_start`:** при создании нового экземпляра потока на каждом уровне вложенности терялось состояние курсора вывода. Если внешняя функция выводила фрагмент без символа переноса строки (`print(..., end="")`), новый экземпляр потока не знал об этом и ошибочно дублировал отступ посреди строки.

Мутация единственного экземпляра `IndentedStream` на протяжении всей цепочки рекурсивных вызовов устраняет обе эти проблемы, сохраняя сложность вывода $O(1)$ относительно глубины стека.

---

## Архитектура решения

Решение состоит из двух взаимодействующих компонентов:

### 1. Поток-заместитель (`IndentedStream`)
Реализует паттерн **Proxy / Decorator** над стандартными потоками вывода (`sys.stdout` и `sys.stderr`):
- Перехватывает метод `.write(text)`.
- Разбивает входящий текст на строки с помощью `splitlines(keepends=True)`, сохраняя символы окончания строк (`\n`).
- Добавляет текущий отступ `self.tab` исключительно в начале строки (`self._at_line_start is True`) и пропускает пустые переводы строк `\n`.
- Отслеживает флаг `self._at_line_start = line.endswith('\n')`, корректно обрабатывая фрагментарный вывод (`end=""`).
- Через `__getattr__` прозрачно делегирует все остальные методы и атрибуты (`fileno`, `encoding`, `flush`) оригинальному потоку.

### 2. Декоратор (`@tracer`)
Управляет жизненным циклом потоков и динамикой отступов:
- **Универсальность вызова:** поддерживает использование как без параметров `@tracer`, так и с настройкой отступа `@tracer(tab='...')`.
- **Контекст корневого вызова (`is_root`):** потоки `sys.stdout` и `sys.stderr` подменяются ровно один раз на нулевом уровне вложенности (`not isinstance(sys.stdout, IndentedStream)`) и гарантированно возвращаются в исходное состояние при выходе из корневого вызова.
- **Прямой ход (спуск):** выводит сообщение о вызове функции с текущим отступом вызывающей стороны, после чего увеличивает отступ: `sys.stdout.tab += tab`.
- **Тело функции и симметричный откат отступа:**
  - В блоке `else:` (выполняется только при успешном завершении без исключений) **сначала** откатывает отступ назад (`sys.stdout.tab = sys.stdout.tab[:-len(tab)]`), и **затем** выводит сообщение о завершении: если функция возвращает `None`, печатается компактное `f'"{func.__name__}" terminated.'`, иначе — полное сообщение со значением и типом `f'"{func.__name__}" terminated. Returned value: {res} (of type {type(res)}).'`. Благодаря этому строки вызова (`call`) и завершения (`terminated`) функции находятся **строго на одном и том же уровне отступа**.
  - В блоке `except:` отступ аналогично сначала откатывается назад, после чего сообщение об ошибке отправляется в `sys.stderr` на уровне вызова упавшей функции, и исключение пробрасывается дальше (`raise`).
- **Очистка ресурсов:** в блоке `finally:` выполняется гарантированное восстановление оригинальных потоков ОС для корневого вызова (`if is_root:`).

---

## Код решения

```python
import functools
import sys
from collections.abc import Callable
from typing import TextIO


class IndentedStream:
    """Обертка над потоком вывода, добавляющая отступ в начале каждой строки."""

    def __init__(
        self, original_stream: 'TextIO | IndentedStream', tab: str = '   '
    ) -> None:
        self.original_stream = original_stream
        self.tab = tab
        self._at_line_start = True

    def write(self, text: str) -> None:
        if not text:
            return
        lines = text.splitlines(keepends=True)
        result = []
        for line in lines:
            if self._at_line_start and line != '\n':
                result.append(self.tab)
            result.append(line)
            self._at_line_start = line.endswith('\n')
        self.original_stream.write(''.join(result))

    def __getattr__(self, name: str) -> object:
        return getattr(self.original_stream, name)


def tracer(_func=None, *, tab: str = '    ') -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            old_stdout, old_stderr = None, None

            is_root = not isinstance(sys.stdout, IndentedStream)
            if is_root:
                old_stdout, old_stderr = sys.stdout, sys.stderr
                sys.stdout = IndentedStream(old_stdout, tab='')
                sys.stderr = IndentedStream(old_stderr, tab='')

            print(f'"{func.__name__}" call with args {args} and kwargs {kwargs}.')
            sys.stdout.tab += tab
            sys.stderr.tab += tab
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                sys.stdout.tab = sys.stdout.tab[: -len(tab)]
                sys.stderr.tab = sys.stderr.tab[: -len(tab)]
                sys.stderr.write(f'"{func.__name__}" raised {type(e).__name__}: {e}\n')
                raise
            else:
                sys.stdout.tab = sys.stdout.tab[: -len(tab)]
                sys.stderr.tab = sys.stderr.tab[: -len(tab)]
                if res is None:
                    print(f'"{func.__name__}" terminated.')
                else:
                    print(
                        f'"{func.__name__}" terminated. Returned value: {res} (of type {type(res)}).'
                    )
                return res
            finally:
                if is_root and old_stdout is not None and old_stderr is not None:
                    sys.stdout, sys.stderr = old_stdout, old_stderr

        return wrapper

    return decorator if _func is None else decorator(_func)
```

---

## Оценка сложности

Обозначим:
- $N$ — максимальная глубина стека рекурсии;
- $K$ — общее количество выполненных вызовов декорированной функции;
- $L$ — суммарная длина выводимых строковых данных.

### Временная сложность (Time Complexity)
- **Накладные расходы на вызов:** на каждом шаге рекурсии конкатенация строк в `sys.stdout.tab += tab` и срез в блоках `else`/`except` занимают время, пропорциональное текущей длине строки отступа: $O(\text{depth} \cdot |tab|)$. Для дерева рекурсии глубиной $N$ это составляет $O(N)$ на шаг.
- **Накладные расходы на вывод:** метод `write()` обрабатывает входящую строку длины $L$ за время $O(L)$, так как текст разбивается за один проход и выводится в оригинальный поток через единый `''.join()`. В отличие от вложенных потоков, время вывода **не умножается на глубину стека**.
- **Итоговая дополнительная временная сложность:** $O(K \cdot N + L)$ в худшем случае (на практике пренебрежимо мала по сравнению с вычислениями внутри функции).

### Пространственная сложность (Space Complexity)
- **Память под перехватчик:** экземпляр `IndentedStream` создается в количестве **ровно 2 штук** (для `stdout` и `stderr`), расходуя константную память $O(1)$.
- **Хранение текущего отступа:** строка `sys.stdout.tab` на глубине рекурсии $N$ занимает $O(N \cdot |tab|)$ дополнительной памяти.
- **Стек вызовов:** каждый вызов `wrapper` добавляет один фрейм в системный стек вызовов Python, что требует $O(N)$ дополнительной памяти на стек (соразмерно глубине рекурсии самой декорируемой функции).
- **Итоговая дополнительная пространственная сложность:** $O(N)$ памяти на стек и хранение строки отступа.

---

## Визуализация и примеры работы

### Пример 1. Разветвленная (древовидная) рекурсия (`fibonacci(3)`)

Линейная рекурсия (вроде факториала) тривиальна и скрывает ключевое достоинство трассировщика — работу с ветвящимися деревьями вызовов. Рассмотрим вычисление чисел Фибоначчи с внутренним выводом:

```python
@tracer
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

fib(3)
```

#### Пошаговая трассировка стека и отступов:

| Шаг | Событие | Глубина стека | `sys.stdout.tab` при выводе | Вывод в консоль |
|:---:|:---|:---:|:---|---|
| 1 | Вызов корня `fib(3)` | 0 | `""` | `"fib" call with args (3,) and kwargs {}.` |
| 2 | Спуск в левую ветвь `fib(2)` | 1 | `"    "` | `    "fib" call with args (2,) and kwargs {}.` |
| 3 | Спуск в `fib(1)` | 2 | `"        "` | `        "fib" call with args (1,) and kwargs {}.` |
| 4 | Завершение `fib(1)` (база) | 2 | `"        "` | `        "fib" terminated. Returned value: 1 (of type <class 'int'>).` |
| 5 | Спуск в правую ветвь `fib(0)` | 2 | `"        "` | `        "fib" call with args (0,) and kwargs {}.` |
| 6 | Завершение `fib(0)` (база) | 2 | `"        "` | `        "fib" terminated. Returned value: 0 (of type <class 'int'>).` |
| 7 | Завершение узла `fib(2)` | 1 | `"    "` | `    "fib" terminated. Returned value: 1 (of type <class 'int'>).` |
| 8 | Спуск в правую ветвь корня `fib(1)` | 1 | `"    "` | `    "fib" call with args (1,) and kwargs {}.` |
| 9 | Завершение `fib(1)` | 1 | `"    "` | `    "fib" terminated. Returned value: 1 (of type <class 'int'>).` |
| 10 | Завершение корня `fib(3)` | 0 | `""` | `"fib" terminated. Returned value: 2 (of type <class 'int'>).` |

**Результирующий консольный вывод:**
```text
"fib" call with args (3,) and kwargs {}.
    "fib" call with args (2,) and kwargs {}.
        "fib" call with args (1,) and kwargs {}.
        "fib" terminated. Returned value: 1 (of type <class 'int'>).
        "fib" call with args (0,) and kwargs {}.
        "fib" terminated. Returned value: 0 (of type <class 'int'>).
    "fib" terminated. Returned value: 1 (of type <class 'int'>).
    "fib" call with args (1,) and kwargs {}.
    "fib" terminated. Returned value: 1 (of type <class 'int'>).
"fib" terminated. Returned value: 2 (of type <class 'int'>).
```
Этот пример наглядно демонстрирует способность декоратора корректно отрабатывать подъемы по стеку и повторные погружения в параллельные ветви без накопления или сбоя отступов.

---

### Пример 2. Трассировка с пользовательским выводом внутри функции

```python
@tracer(tab="| ")
def compute(step: int) -> None:
    print(f"step {step} in progress")
    if step > 1:
        compute(step - 1)
    print(f"step {step} done")

compute(2)
```

**Результирующий консольный вывод:**
```text
"compute" call with args (2,) and kwargs {}.
| step 2 in progress
| "compute" call with args (1,) and kwargs {}.
| | step 1 in progress
| | step 1 done
| "compute" terminated.
| step 2 done
"compute" terminated.
```
Все пользовательские вызовы `print` аккуратно вписаны внутрь соответствующих блоков: вход и выход функции находятся на одном уровне, а тело сдвинуто на один шаг вправо.

---

### Пример 3. Обработка исключений в `sys.stderr`

```python
@tracer
def broken(n: int):
    if n == 0:
        raise ValueError("Critical zero")
    broken(n - 1)

broken(1)
```

**Вывод:**
```text
[stdout] "broken" call with args (1,) and kwargs {}.
[stdout]     "broken" call with args (0,) and kwargs {}.
[stderr]     "broken" raised ValueError: Critical zero
[stderr] "broken" raised ValueError: Critical zero
Traceback (most recent call last):
    ...
ValueError: Critical zero
```
Сообщение об ошибке выводится на том же уровне отступа, что и вызов функции, в которой она произошла.
