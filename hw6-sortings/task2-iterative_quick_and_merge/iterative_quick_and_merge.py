def merge_sort_iterative(arr: list) -> list:
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

    width = 1
    n = len(arr_copy)
    while width < n:
        for lo in range(0, n - width, width * 2):
            mid = lo + width - 1
            hi = min(lo + 2 * width - 1, n - 1)
            if arr_copy[mid] > arr_copy[mid + 1]:
                _merge(lo, mid, hi)
        width *= 2

    return arr_copy


def quick_sort_iterative(arr: list) -> list:
    arr_copy = arr.copy()
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()

        if hi <= lo:
            continue

        pivot = arr_copy[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr_copy[j] <= pivot:
                i += 1
                arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]

        i += 1
        arr_copy[i], arr_copy[hi] = arr_copy[hi], arr_copy[i]

        stack.append((lo, i - 1))
        stack.append((i + 1, hi))

    return arr_copy
