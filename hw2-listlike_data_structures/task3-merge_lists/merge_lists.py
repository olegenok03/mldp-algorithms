import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from stack_vs_queue import UDL, ListNode


def merge_sorted_lists_v1(
    node1: ListNode | None, node2: ListNode | None
) -> ListNode | None:
    cur_node = dummy = ListNode(0, None)
    while node1 and node2:
        if node1.val < node2.val:
            cur_node.next = node1
            cur_node = cur_node.next
            node1 = node1.next
        else:
            cur_node.next = node2
            cur_node = cur_node.next
            node2 = node2.next

    cur_node.next = node1 or node2

    new_head = dummy.next
    del dummy
    return new_head


def merge_sorted_lists_v2(
    node1: ListNode | None, node2: ListNode | None
) -> ListNode | None:
    if not node1:
        return node2
    if not node2:
        return node1

    if node1.val < node2.val:
        cur_node = new_head = node1
        node1 = cur_node.next
    else:
        cur_node = new_head = node2
        node2 = cur_node.next

    while node1 and node2:
        if node1.val < node2.val:
            cur_node.next = node1
            cur_node = cur_node.next
            node1 = node1.next
        else:
            cur_node.next = node2
            cur_node = cur_node.next
            node2 = node2.next

    cur_node.next = node1 or node2

    return new_head


if __name__ == '__main__':
    arr1 = [int(x) for x in input().split()]
    arr2 = [int(x) for x in input().split()]
    answer = sorted(arr1 + arr2)

    merged_head_v1 = merge_sorted_lists_v1(UDL(arr1)._head, UDL(arr2)._head)
    merged_head_v2 = merge_sorted_lists_v2(UDL(arr1)._head, UDL(arr2)._head)

    merged_list_v1 = UDL.from_head_list_node(merged_head_v1)
    merged_list_v2 = UDL.from_head_list_node(merged_head_v2)

    assert repr(merged_list_v1) == repr(merged_list_v2)
    assert list(map(int, repr(merged_list_v1).split())) == answer
    print(merged_list_v1)
