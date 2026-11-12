import random


def kth_maximum(arr: list, k: int) -> int:
    arr_copy = arr.copy()
    target_idx = k - 1
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        pivot_idx = random.randint(lo, hi)
        arr_copy[pivot_idx], arr_copy[hi] = arr_copy[hi], arr_copy[pivot_idx]
        pivot = arr_copy[hi]

        i = lo - 1
        for j in range(lo, hi):
            if arr_copy[j] >= pivot:
                i += 1
                arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]

        i += 1
        arr_copy[i], arr_copy[hi] = arr_copy[hi], arr_copy[i]

        if i == target_idx:
            return arr_copy[i]
        elif i > target_idx:
            hi = i - 1
        else:
            lo = i + 1
    return arr_copy[target_idx]


if __name__ == '__main__':
    assert kth_maximum([3, 2, 1, 5, 6, 4], 2) == 5
    assert kth_maximum([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
