import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import pytest
from tracer import IndentedStream, tracer


def test_factorial_call_and_return_tracing(capsys: pytest.CaptureFixture[str]) -> None:
    @tracer
    def factorial(n: int) -> int:
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    result = factorial(3)
    assert result == 6

    captured = capsys.readouterr()
    expected_lines = [
        '"factorial" call with args (3,) and kwargs {}.',
        '    "factorial" call with args (2,) and kwargs {}.',
        '        "factorial" call with args (1,) and kwargs {}.',
        '        "factorial" terminated. Returned value: 1 (of type <class \'int\'>).',
        '    "factorial" terminated. Returned value: 2 (of type <class \'int\'>).',
        '"factorial" terminated. Returned value: 6 (of type <class \'int\'>).',
    ]
    actual_lines = [line for line in captured.out.splitlines() if line.strip()]
    assert actual_lines == expected_lines


def test_decorator_usage_variants(capsys: pytest.CaptureFixture[str]) -> None:
    # 1. @tracer без скобок
    @tracer
    def func_a(x: int) -> int:
        return x + 1

    # 2. @tracer() с пустыми скобками
    @tracer()
    def func_b(x: int) -> int:
        return x * 2

    # 3. @tracer(tab='..') с кастомным отступом
    @tracer(tab='..')
    def func_c(x: int) -> int:
        if x > 0:
            return func_c(x - 1)
        return 0

    assert func_a(1) == 2
    assert func_b(3) == 6
    assert func_c(2) == 0

    captured = capsys.readouterr()
    out = captured.out
    assert '"func_a" call with args (1,) and kwargs {}.' in out
    assert '"func_b" call with args (3,) and kwargs {}.' in out
    assert '.."func_c" call with args (1,) and kwargs {}.' in out
    assert '...."func_c" call with args (0,) and kwargs {}.' in out


def test_inner_prints_are_indented(capsys: pytest.CaptureFixture[str]) -> None:
    @tracer(tab='| ')
    def compute(step: int) -> None:
        print(f'step {step} in progress')
        if step > 1:
            compute(step - 1)
        print(f'step {step} done')

    compute(2)
    captured = capsys.readouterr()
    expected_lines = [
        '"compute" call with args (2,) and kwargs {}.',
        '| step 2 in progress',
        '| "compute" call with args (1,) and kwargs {}.',
        '| | step 1 in progress',
        '| | step 1 done',
        '| "compute" terminated.',
        '| step 2 done',
        '"compute" terminated.',
    ]
    actual_lines = [line for line in captured.out.splitlines() if line.strip()]
    assert actual_lines == expected_lines


def test_multiline_and_partial_prints(capsys: pytest.CaptureFixture[str]) -> None:
    @tracer(tab='  ')
    def display_multi() -> None:
        print('line 1\nline 2')
        print('part 1 - ', end='')
        print('part 2')

    display_multi()
    captured = capsys.readouterr()
    expected_lines = [
        '"display_multi" call with args () and kwargs {}.',
        '  line 1',
        '  line 2',
        '  part 1 - part 2',
        '"display_multi" terminated.',
    ]
    actual_lines = [line for line in captured.out.splitlines() if line.strip()]
    assert actual_lines == expected_lines


def test_exception_handling_and_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    @tracer
    def broken_func(n: int) -> int:
        if n == 0:
            raise ValueError('Zero is not allowed')
        return broken_func(n - 1)

    with pytest.raises(ValueError, match='Zero is not allowed'):
        broken_func(1)

    captured = capsys.readouterr()
    assert '"broken_func" call with args (1,) and kwargs {}.' in captured.out
    assert '    "broken_func" call with args (0,) and kwargs {}.' in captured.out

    # Ошибка должна быть записана в stderr на том же уровне отступа, что и вызов функции
    assert '    "broken_func" raised ValueError: Zero is not allowed' in captured.err

    # Потоки должны быть полностью возвращены в исходное состояние
    assert not isinstance(sys.stdout, IndentedStream)
    assert not isinstance(sys.stderr, IndentedStream)


def test_mutual_recursion(capsys: pytest.CaptureFixture[str]) -> None:
    @tracer
    def ping(n: int) -> str:
        if n <= 0:
            return 'done'
        return pong(n - 1)

    @tracer
    def pong(n: int) -> str:
        if n <= 0:
            return 'done'
        return ping(n - 1)

    res = ping(2)
    assert res == 'done'

    captured = capsys.readouterr()
    expected_lines = [
        '"ping" call with args (2,) and kwargs {}.',
        '    "pong" call with args (1,) and kwargs {}.',
        '        "ping" call with args (0,) and kwargs {}.',
        '        "ping" terminated. Returned value: done (of type <class \'str\'>).',
        '    "pong" terminated. Returned value: done (of type <class \'str\'>).',
        '"ping" terminated. Returned value: done (of type <class \'str\'>).',
    ]
    actual_lines = [line for line in captured.out.splitlines() if line.strip()]
    assert actual_lines == expected_lines


def test_kwargs_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    @tracer
    def greet(name: str, shout: bool = False) -> str:
        return f'{name.upper() if shout else name}'

    result = greet(name='Antigravity', shout=True)
    assert result == 'ANTIGRAVITY'

    captured = capsys.readouterr()
    assert (
        '"greet" call with args () and kwargs {\'name\': \'Antigravity\', \'shout\': True}.'
        in captured.out
    )
    assert '"greet" terminated. Returned value: ANTIGRAVITY (of type <class \'str\'>).' in captured.out
