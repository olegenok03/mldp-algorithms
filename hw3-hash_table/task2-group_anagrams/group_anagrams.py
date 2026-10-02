from collections import defaultdict
from collections.abc import Hashable

ALPHABET_SIZE = 26
FIRST_LITERAL_CHAR = 'a'


def unordered_string_hash(word: str) -> Hashable:
    hash = [0] * ALPHABET_SIZE
    word = word.lower()
    for char in word:
        hash[ord(char) - ord(FIRST_LITERAL_CHAR)] += 1
    return tuple(hash)


def group_anagrams(words: list[str]) -> list[list[str]]:
    hash_to_group = defaultdict(list)
    for word in words:
        hash_to_group[unordered_string_hash(word)].append(word)
    return list(hash_to_group.values())


if __name__ == '__main__':
    words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
    result = group_anagrams(words)
    print(result)
