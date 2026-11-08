import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from tracer import tracer


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


if __name__ == '__main__':
    print(get_permutations([3, 2, 1]))
    print(get_permutations_inplace([3, 2, 1]))
