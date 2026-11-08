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
