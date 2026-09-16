def primes_counter(max_num: int) -> int:
    is_prime = [True for _ in range(max_num + 1)]
    is_prime[0], is_prime[1] = False, False

    for k in range(2, int(max_num ** (1 / 2)) + 1):
        if is_prime[k]:
            for i in range(k * k, max_num + 1, k):
                is_prime[i] = False

    return sum(is_prime)


if __name__ == '__main__':
    max_num = int(input())
    result = primes_counter(max_num)
    print(result)
