from collections.abc import Iterable
from copy import copy


class ListNode:
    def __init__(self, val: int, next: 'ListNode|None' = None) -> None:
        self.val = val
        self.next = next


class UDL:
    def __init__(self, iterable: Iterable | None = None) -> None:
        self._head = self._tail = None
        self._len = 0
        if iterable is not None:
            for val in iterable:
                self.append_right(val)

    @classmethod
    def from_head_list_node(cls, head: ListNode | None) -> 'UDL':
        new_list = UDL()
        new_list._head = cur_node = head
        new_list._len = 0
        while cur_node:
            new_list._len += 1
            new_list._tail = cur_node
            cur_node = cur_node.next
        return new_list

    def __copy__(self) -> 'UDL':
        new_list = UDL()
        if self._head is None or self._tail is None:
            return new_list

        cur_node = self._head
        for _ in range(self._len):
            new_list.append_right(cur_node.val)
            cur_node = cur_node.next
        return new_list

    def __len__(self):
        return self._len

    def __repr__(self) -> str:
        values = []
        cur_node = self._head
        while cur_node != None:
            values.append(cur_node.val)
            cur_node = cur_node.next

        return ' '.join(map(str, values))

    def append_right(self, val: int) -> None:
        new_node = ListNode(val)
        self._len += 1
        if self._head is None or self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

    def append_left(self, val: int) -> None:
        new_node = ListNode(val, self._head)
        self._len += 1
        self._head = new_node
        if self._tail is None:
            self._tail = new_node

    def pop_right(self) -> int:
        if self._head is None or self._tail is None:
            raise IndexError('pop from empty list')

        if self._len == 1:
            popped = self._head
            val = popped.val

            self._head = self._tail = None
            self._len = 0

            del popped
            return val

        prev_node = self._head
        for _ in range(self._len - 2):
            prev_node = prev_node.next

        popped = prev_node.next
        val = popped.val

        prev_node.next = None
        self._tail = prev_node
        self._len -= 1

        del popped
        return val

    def pop_left(self) -> int:
        if self._head is None or self._tail is None:
            raise IndexError('pop from empty list')

        if self._len == 1:
            popped = self._head
            val = popped.val

            self._head = self._tail = None
            self._len = 0

            del popped
            return val

        popped = self._head
        val = popped.val

        next_node = popped.next
        self._head = next_node
        self._len -= 1

        del popped
        return val

    def peek_left(self) -> int:
        if self._head is None or self._tail is None:
            raise IndexError('peek from empty list')
        return self._head.val

    def peek_right(self) -> int:
        if self._head is None or self._tail is None:
            raise IndexError('peek from empty list')
        return self._tail.val


class MyQueue:
    def __init__(self, iterable: Iterable | None = None) -> None:
        self._udl = UDL(iterable)

    def __copy__(self) -> 'MyQueue':
        new_queue = MyQueue()
        new_queue._udl = copy(self._udl)
        return new_queue

    def __len__(self):
        return len(self._udl)

    def __repr__(self) -> str:
        return repr(self._udl)

    def peek(self):
        return self._udl.peek_left()

    def push(self, val: int):
        return self._udl.append_right(val)

    def pop(self):
        return self._udl.pop_left()


class MyStack:
    def __init__(self, iterable: Iterable | None = None) -> None:
        self._udl = UDL(iterable)

    def __copy__(self) -> 'MyStack':
        new_stack = MyStack()
        new_stack._udl = copy(self._udl)
        return new_stack

    def __len__(self):
        return len(self._udl)

    def __repr__(self) -> str:
        return repr(self._udl)

    def peek(self):
        return self._udl.peek_left()

    def push(self, val: int):
        return self._udl.append_left(val)

    def pop(self):
        return self._udl.pop_left()
