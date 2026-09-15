class ListNode:
    def __init__(self, val: int, next: "ListNode|None") -> None:
        self.val = val
        self.next = next


class UDL:
    def __init__(
        self, head: ListNode | None = None, tail: ListNode | None = None
    ) -> None:
        self.head = head
        self.tail = tail

    def __repr__(self) -> str:
        values = []
        cur_node = self.head
        while cur_node != None:
            values.append(cur_node.val)
            cur_node = cur_node.next

        return ' '.join(map(str, values))

    def reverse(self) -> None:
        if self.head is None:
            return

        def reverse_list_rec(head: ListNode | None = None) -> None:
            if head is None or head.next is None:
                return
            cur_next = head.next
            reverse_list_rec(cur_next)
            cur_next.next = head

        reverse_list_rec(self.head)
        new_tail = self.head
        new_tail.next = None
        self.head = self.tail
        self.tail = new_tail


if __name__ == '__main__':
    node4 = ListNode(4, None)
    node3 = ListNode(3, node4)
    node2 = ListNode(2, node3)
    node1 = ListNode(1, node2)
    udl = UDL(node1, node4)
    udl.reverse()
    print(udl)
    print(udl.tail.next is None)
