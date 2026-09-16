def max_even_sum(numbers: list) -> int:
    if not numbers:
        return 0
    max_sum = 0
    odd_min = 0
    for n in numbers:
        max_sum += n
        if n % 2 != 0 and (n < odd_min or not odd_min):
            odd_min = n
    if max_sum % 2 == 0:
        return max_sum
    else:
        return max_sum - odd_min


if __name__ == '__main__':
    numbers = [int(x) for x in input().split()]
    result = max_even_sum(numbers)
    print(result)
