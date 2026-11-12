import time
from functools import wraps


def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return res, elapsed

    return wrapper


def merge_sort_recursive(arr: list) -> list:
    if len(arr) <= 1:
        return arr.copy()

    arr_copy = arr.copy()
    aux = [0] * len(arr_copy)

    def _merge(lo: int, mid: int, hi: int) -> None:
        aux[lo : mid + 1] = arr_copy[lo : mid + 1]

        i, j, k = lo, mid + 1, lo

        while i <= mid and j <= hi:
            if arr_copy[j] < aux[i]:
                arr_copy[k] = arr_copy[j]
                j += 1
            else:
                arr_copy[k] = aux[i]
                i += 1
            k += 1

        if i <= mid:
            arr_copy[k : hi + 1] = aux[i : mid + 1]

    def _merge_sort_rec_inplace(lo: int, hi: int) -> None:
        if hi <= lo:
            return

        mid = lo + (hi - lo) // 2

        _merge_sort_rec_inplace(lo, mid)
        _merge_sort_rec_inplace(mid + 1, hi)

        if arr_copy[mid] <= arr_copy[mid + 1]:
            return

        _merge(lo, mid, hi)

    _merge_sort_rec_inplace(0, len(arr_copy) - 1)
    return arr_copy


def quick_sort_recursive(arr: list) -> list:
    arr_copy = arr.copy()

    def _quick_sort_rec_inplace(lo: int, hi: int) -> None:
        if hi <= lo:
            return

        pivot = arr_copy[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr_copy[j] <= pivot:
                i += 1
                arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]

        i += 1
        arr_copy[i], arr_copy[hi] = arr_copy[hi], arr_copy[i]

        _quick_sort_rec_inplace(lo, i - 1)
        _quick_sort_rec_inplace(i + 1, hi)

    _quick_sort_rec_inplace(0, len(arr_copy) - 1)
    return arr_copy
