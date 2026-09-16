import pytest
from palindrome import is_palindrome

testdata_simple = [
    (123321, True),
    (12321, True),
    (666, True),
    (666666, True),
    (int('6' * 1000), True),
    (123333, False),
    (665666, False),
]

testdata_digits = [(1, True), (9, True), (5, True)]

testdata_with_zeros = [
    (101, True),
    (1001, True),
    (10, False),
    (1000, False),
    (1001001, True),
    (605070606, False),
]


@pytest.mark.parametrize('number,number_is_palindrome', testdata_simple)
def test_is_palindrome_simple_numbers(number: int, number_is_palindrome: bool) -> None:
    answer = is_palindrome(number)
    assert answer == number_is_palindrome


@pytest.mark.parametrize('number,number_is_palindrome', testdata_digits)
def test_is_palindrome_digits(number: int, number_is_palindrome: bool) -> None:
    answer = is_palindrome(number)
    assert answer == number_is_palindrome


@pytest.mark.parametrize('number,number_is_palindrome', testdata_with_zeros)
def test_is_palindrome_numbers_with_zeros(
    number: int, number_is_palindrome: bool
) -> None:
    answer = is_palindrome(number)
    assert answer == number_is_palindrome
