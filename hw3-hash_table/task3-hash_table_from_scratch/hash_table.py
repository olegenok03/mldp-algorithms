from collections.abc import Hashable, Iterable, Iterator, Mapping
from functools import singledispatchmethod
from typing import TypeVar

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')

HASH_TABLE_INITIAL_CAPACITY = 8


class HashTableKeysView[K]:
    def __init__(self, hash_table: 'HashTable'):
        self._hash_table = hash_table

    def __len__(self) -> int:
        return len(self._hash_table)

    def __iter__(self) -> Iterator[K]:
        for chain in self._hash_table._table:
            for key, _ in chain:
                yield key

    def __contains__(self, key: K) -> bool:
        return key in self._hash_table


class HashTableValuesView[V]:
    def __init__(self, hash_table: 'HashTable'):
        self._hash_table = hash_table

    def __len__(self) -> int:
        return len(self._hash_table)

    def __iter__(self) -> Iterator[V]:
        for chain in self._hash_table._table:
            for _, value in chain:
                yield value


class HashTableItemsView[K, V]:
    def __init__(self, hash_table: 'HashTable'):
        self._hash_table = hash_table

    def __len__(self) -> int:
        return len(self._hash_table)

    def __iter__(self) -> Iterator[tuple[K, V]]:
        for chain in self._hash_table._table:
            yield from chain


class HashTable[K: Hashable, V]:
    def __init__(
        self,
        items: Iterable[tuple[K, V]] | Mapping[K, V] | None = None,
        min_load_factor: float = 0.25,
        max_load_factor: float = 0.9,
    ) -> None:
        self._size = 0
        self._capacity = HASH_TABLE_INITIAL_CAPACITY
        self.min_load_factor = min_load_factor
        self.max_load_factor = max_load_factor
        self._table: list[list[tuple[K, V]]] = [[] for _ in range(self._capacity)]
        if items is not None:
            self.update(items)

    def items(self) -> HashTableItemsView[K, V]:
        return HashTableItemsView(self)

    def keys(self) -> HashTableKeysView[K]:
        return HashTableKeysView(self)

    def values(self) -> HashTableValuesView[V]:
        return HashTableValuesView(self)

    def _get_index_by_key(self, key: K) -> int:
        return hash(key) % self._capacity

    def _rebuild(self) -> None:
        if self._size / self._capacity > self.max_load_factor:
            self._capacity *= 2
        elif (
            self._capacity > HASH_TABLE_INITIAL_CAPACITY
            and self._size / self._capacity < self.min_load_factor
        ):
            self._capacity //= 2
        else:
            return

        new_table = [[] for _ in range(self._capacity)]
        for chain in self._table:
            for key, value in chain:
                new_index = self._get_index_by_key(key)
                new_table[new_index].append((key, value))
        self._table = new_table

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[K]:
        return iter(self.keys())

    def __contains__(self, key: K) -> bool:
        index = self._get_index_by_key(key)
        for old_key, _ in self._table[index]:
            if old_key == key:
                return True
        return False

    def __getitem__(self, key: K) -> V:
        index = self._get_index_by_key(key)
        for existing_key, existing_value in self._table[index]:
            if existing_key == key:
                return existing_value
        raise KeyError(f'Unknown key: {key}')

    def __setitem__(self, key: K, value: V) -> None:
        index = self._get_index_by_key(key)
        for j, (old_key, _) in enumerate(self._table[index]):
            if old_key == key:
                self._table[index][j] = (key, value)
                return
        self._size += 1
        self._rebuild()
        index = self._get_index_by_key(key)
        self._table[index].append((key, value))

    @singledispatchmethod
    def update(self, new_items: object):
        raise NotImplementedError(f'Unknown type: {type(new_items)}')

    @update.register
    def _(self, new_items: Iterable):
        for key, value in new_items:
            self.__setitem__(key, value)

    @update.register
    def _(self, new_items: Mapping):
        for key, value in new_items.items():
            self.__setitem__(key, value)

    def __delitem__(self, key: K) -> None:
        index = self._get_index_by_key(key)
        for j, (existing_key, _) in enumerate(self._table[index]):
            if existing_key == key:
                self._table[index].pop(j)
                self._size -= 1
                self._rebuild()
                return
        raise KeyError(f'Unknown key: {key}')

    def __repr__(self) -> str:
        pairs = [f'{k}: {v}' for k, v in self.items()]
        return '{' + ', '.join(pairs) + '}'


if __name__ == '__main__':
    a = HashTable({1: 0, 'a': 0})
    print(a)
