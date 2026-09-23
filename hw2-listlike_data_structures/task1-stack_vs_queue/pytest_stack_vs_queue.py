import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from stack_vs_queue import UDL, MyQueue, MyStack


class TestUDL:
    """Группа тестов для базового класса односвязного списка."""

    def test_udl_initialization(self):
        """Проверка инициализации: пустой список и список из итерируемого объекта."""
        empty_udl = UDL()
        assert len(empty_udl) == 0

        iter_udl = UDL([1, 2, 3])
        assert len(iter_udl) == 3
        assert repr(iter_udl) == '1 2 3'

    def test_udl_append_and_pop_left(self):
        """Проверка добавления и извлечения элементов с левого края."""
        udl = UDL()
        udl.append_left(10)
        udl.append_left(20)

        assert len(udl) == 2
        assert udl.peek_left() == 20
        assert udl.pop_left() == 20
        assert udl.pop_left() == 10
        assert len(udl) == 0

    def test_udl_append_and_pop_right(self):
        """Проверка добавления и извлечения элементов с правого края."""
        udl = UDL()
        udl.append_right(10)
        udl.append_right(20)

        assert len(udl) == 2
        assert udl.peek_right() == 20
        assert udl.pop_right() == 20
        assert udl.pop_right() == 10
        assert len(udl) == 0

    def test_udl_copy(self):
        """Проверка корректности создания копии списка."""
        udl = UDL([1, 2, 3])
        udl_copy = udl.__copy__()

        assert repr(udl) == repr(udl_copy)

        udl.pop_left()
        assert len(udl) == 2
        assert len(udl_copy) == 3

    def test_udl_exceptions_on_empty(self):
        """Проверка возникновения исключений при обращении к пустому списку."""
        udl = UDL()
        with pytest.raises(IndexError, match='pop from empty list'):
            udl.pop_left()

        with pytest.raises(IndexError, match='pop from empty list'):
            udl.pop_right()

        with pytest.raises(IndexError, match='peek from empty list'):
            udl.peek_left()

        with pytest.raises(IndexError, match='peek from empty list'):
            udl.peek_right()


class TestMyStack:
    """Группа тестов для класса стека."""

    def test_stack_standard_operations(self):
        """Проверка стандартного сценария LIFO."""
        stack = MyStack()
        stack.push(1)
        stack.push(2)
        stack.push(3)

        assert len(stack) == 3
        assert stack.peek() == 3
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1
        assert len(stack) == 0

    def test_stack_initialization_and_utility(self):
        """Проверка инициализации из итерируемого объекта и служебных методов."""
        stack = MyStack([10, 20])
        # При инициализации из итерабельного объекта (согласно реализации UDL)
        # элементы добавляются вправо, но стек работает слева.
        # Поэтому первым на выход пойдет 10, так как он на левом конце.
        assert len(stack) == 2
        assert repr(stack) == '10 20'

        stack_copy = stack.__copy__()
        assert repr(stack_copy) == '10 20'

    def test_stack_exceptions(self):
        """Проверка исключений при попытке извлечь элемент из пустого стека."""
        stack = MyStack()
        with pytest.raises(IndexError):
            stack.pop()
        with pytest.raises(IndexError):
            stack.peek()


class TestMyQueue:
    """Группа тестов для класса очереди."""

    def test_queue_standard_operations(self):
        """Проверка стандартного сценария FIFO."""
        queue = MyQueue()
        queue.push(1)
        queue.push(2)
        queue.push(3)

        assert len(queue) == 3
        assert queue.peek() == 1
        assert queue.pop() == 1
        assert queue.pop() == 2
        assert queue.pop() == 3
        assert len(queue) == 0

    def test_queue_initialization_and_utility(self):
        """Проверка инициализации из итерируемого объекта и служебных методов."""
        queue = MyQueue([10, 20])
        assert len(queue) == 2
        assert repr(queue) == '10 20'

        queue_copy = queue.__copy__()
        assert repr(queue_copy) == '10 20'

    def test_queue_exceptions(self):
        """Проверка исключений при попытке извлечь элемент из пустой очереди."""
        queue = MyQueue()
        with pytest.raises(IndexError):
            queue.pop()
        with pytest.raises(IndexError):
            queue.peek()
