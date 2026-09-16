import pytest
from primes_counter import primes_counter

testdata_simple = [
    (10, 4),
    (175, 40),
    (3500, 489),
]

testdata_prime_boundary = [(11, 5), (179, 41), (3571, 500)]

testdata_squares = [(25, 9), (36, 11), (49, 15)]


@pytest.mark.parametrize('max_num,primes_count', testdata_simple)
def test_primes_counter_simple_sums(max_num: int, primes_count: int) -> None:
    answer = primes_counter(max_num)
    assert answer == primes_count


@pytest.mark.parametrize('max_num,primes_count', testdata_prime_boundary)
def test_primes_counter_with_prime_boundary(max_num: int, primes_count: int) -> None:
    answer = primes_counter(max_num)
    assert answer == primes_count

@pytest.mark.parametrize('max_num,primes_count', testdata_squares)
def test_primes_counter_with_square_boundary(max_num: int, primes_count: int) -> None:
    answer = primes_counter(max_num)
    assert answer == primes_count
