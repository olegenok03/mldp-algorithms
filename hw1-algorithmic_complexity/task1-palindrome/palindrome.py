from math import log10


def is_palindrome(a: int) -> bool:
    ord_num = int(log10(a)) + 1
    for i in range(ord_num // 2):
        if (a // 10 ** i) % 10 != (a // 10 ** (ord_num - i - 1)) % 10:
            return False
    return True


if __name__ == '__main__':
    a = int(input())
    c = is_palindrome(a)
    print(c)
