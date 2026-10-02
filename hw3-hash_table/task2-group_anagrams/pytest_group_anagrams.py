import pytest
from group_anagrams import group_anagrams

testdata_unique = [
    (
        ['eat', 'tea', 'tan', 'ate', 'nat', 'bat'],
        [['bat'], ['nat', 'tan'], ['ate', 'eat', 'tea']],
    ),
    ([''], [['']]),
    (['a'], [['a']]),
    (['abc', 'def', 'ghi'], [['abc'], ['def'], ['ghi']]),
]

testdata_duplicates = [
    (['a', 'a', 'a'], [['a', 'a', 'a']]),
    (['', '', ''], [['', '', '']]),
    (['ab', 'ba', 'ab', 'ba'], [['ab', 'ab', 'ba', 'ba']]),
]

testdata_long_strings = [
    (['b' * k for k in range(1, 1000)], [['b' * k] for k in range(1, 1000)]),
    (
        ['aabbcc' * 1000, 'ccbbaa' * 1000, 'abcabc' * 1000, 'abccba' * 1000],
        [['aabbcc' * 1000, 'ccbbaa' * 1000, 'abcabc' * 1000, 'abccba' * 1000]],
    ),
]


@pytest.mark.parametrize(
    'words,expected',
    testdata_unique + testdata_duplicates + testdata_long_strings,
)
def test_group_anagrams(words: list[str], expected: list[list[str]]) -> None:
    result = group_anagrams(words)

    sorted_result = sorted([sorted(group) for group in result])
    sorted_expected = sorted([sorted(group) for group in expected])

    assert sorted_result == sorted_expected
