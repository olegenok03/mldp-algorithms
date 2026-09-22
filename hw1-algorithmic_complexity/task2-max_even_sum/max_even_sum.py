def max_even_sum(numbers: list) -> int:
    if not numbers:
        return 0
    max_sum = 0
    odd_min = None
    for n in numbers:
        max_sum += n
        if n % 2 != 0 and (odd_min is None or n < odd_min):
            odd_min = n
    if max_sum % 2 == 0: # необходимое условие для 'odd_min is None == True'
        return max_sum
    else:
        return max_sum - odd_min


if __name__ == '__main__':
    numbers = [int(x) for x in input().split()]
    result = max_even_sum(numbers)
    print(result)
