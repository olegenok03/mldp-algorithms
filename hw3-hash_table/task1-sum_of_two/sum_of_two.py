def find_two_summands(arr: list[int], k: int) -> tuple[int, int]:
    residuals = {}
    for i, num in enumerate(arr):
        if num in residuals:
            return residuals[num], i
        residuals[k - num] = i
    raise ValueError('Summands have not found')


if __name__ == '__main__':
    arr = list(map(int, input().split()))
    k = int(input())
    i, j = find_two_summands(arr, k)
    print(i, j)
