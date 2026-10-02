import pytest
from hash_table import (
    HASH_TABLE_INITIAL_CAPACITY,
    HashTable,
    HashTableItemsView,
    HashTableKeysView,
    HashTableValuesView,
)

# --- 1. Тесты инициализации ---


def test_init_empty():
    """Тест создания пустой хеш-таблицы."""
    ht = HashTable()
    assert len(ht) == 0
    assert ht._capacity == HASH_TABLE_INITIAL_CAPACITY


def test_init_with_mapping():
    """Тест инициализации с использованием словаря (Mapping)."""
    ht = HashTable({'a': 1, 'b': 2})
    assert len(ht) == 2
    assert ht['a'] == 1
    assert ht['b'] == 2


def test_init_with_iterable():
    """Тест инициализации с использованием списка кортежей (Iterable)."""
    ht = HashTable([('a', 1), ('b', 2)])
    assert len(ht) == 2
    assert ht['a'] == 1


# --- 2. Тесты базовых операций (CRUD) и Dunder-методов ---


def test_set_and_get_item():
    """Тест добавления и получения элементов."""
    ht = HashTable()
    ht['key1'] = 'value1'
    ht['key2'] = 'value2'
    assert ht['key1'] == 'value1'
    assert ht['key2'] == 'value2'
    assert len(ht) == 2


def test_update_existing_key():
    """Тест обновления значения по существующему ключу."""
    ht = HashTable({'key': 'old_value'})
    ht['key'] = 'new_value'
    assert ht['key'] == 'new_value'
    assert len(ht) == 1


def test_del_item():
    """Тест удаления элемента."""
    ht = HashTable({'a': 1, 'b': 2})
    del ht['a']
    assert 'a' not in ht
    assert len(ht) == 1
    with pytest.raises(KeyError):
        _ = ht['a']


def test_missing_key_raises_keyerror():
    """Тест вызова KeyError при обращении и удалении несуществующего ключа."""
    ht = HashTable()
    with pytest.raises(KeyError):
        _ = ht['missing']
    with pytest.raises(KeyError):
        del ht['missing']


def test_contains():
    """Тест оператора in (__contains__)."""
    ht = HashTable({'a': 1})
    assert 'a' in ht
    assert 'b' not in ht


def test_iteration():
    """Тест прямой итерации по хеш-таблице (должна возвращать ключи)."""
    ht = HashTable({'a': 1, 'b': 2})
    keys = list(iter(ht))
    assert len(keys) == 2
    assert 'a' in keys
    assert 'b' in keys


# --- 3. Тесты обработки коллизий ---


class MockCollidingKey:
    """Служебный класс для имитации одинаковых хешей (коллизий)."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, MockCollidingKey) and self.name == other.name


def test_collisions():
    """Тест цепочек (chaining): ключи с одинаковым хешем должны корректно сохраняться и извлекаться."""
    ht = HashTable()
    key1 = MockCollidingKey('first')
    key2 = MockCollidingKey('second')

    ht[key1] = 'value1'
    ht[key2] = 'value2'

    assert len(ht) == 2
    assert ht[key1] == 'value1'
    assert ht[key2] == 'value2'

    # Удаление одного из коллизирующих элементов
    del ht[key1]
    assert len(ht) == 1
    assert ht[key2] == 'value2'
    with pytest.raises(KeyError):
        _ = ht[key1]


def test_rebuild_with_massive_collisions():
    """Тест перестроения таблицы при наличии большого количества коллизий."""
    ht = HashTable()
    initial_capacity = ht._capacity  # Базовая емкость = 8

    # Генерируем 14 ключей с одинаковым хешем
    keys = [MockCollidingKey(f'key_{i}') for i in range(14)]

    # Вставляем элементы. На 8-м элементе (8 / 8 = 1.0 > 0.9) произойдет _rebuild
    for i, key in enumerate(keys):
        ht[key] = i

    # 1. Проверяем, что рехеширование действительно произошло
    assert ht._capacity > initial_capacity
    assert ht._capacity == 16  # Емкость удвоилась (8 -> 16)
    assert len(ht) == 14

    # 2. Проверяем целостность данных после _rebuild
    for i, key in enumerate(keys):
        assert ht[key] == i

    # 3. White-box проверка внутреннего состояния:
    # Поскольку хеш у всех ключей 42, все элементы должны оказаться ровно в одной корзине
    # (по индексу 42 % 16 = 10)
    non_empty_chains = [chain for chain in ht._table if chain]
    assert len(non_empty_chains) == 1, (
        'Все коллизирующие ключи должны лежать в одном chain'
    )
    assert len(non_empty_chains[0]) == 14, 'Chain должен содержать ровно 14 элементов'

    # 4. Проверяем удаление из длинного chain с последующим рехешированием вниз
    # Удаляем 11 элементов, чтобы размер стал 3.
    # При емкости 16 load_factor станет 3/16 = 0.1875, что меньше min_load_factor (0.25).
    # Должен произойти _rebuild с уменьшением емкости (16 -> 8).
    for i in range(11):
        del ht[keys[i]]

    assert len(ht) == 3
    assert ht._capacity == 8  # Емкость вернулась к базовой

    # Убеждаемся, что оставшиеся элементы не пострадали
    assert ht[keys[11]] == 11
    assert ht[keys[12]] == 12
    assert ht[keys[13]] == 13


# --- 4. Тесты динамического масштабирования (_rebuild) ---


def test_rebuild_scale_up():
    """Тест увеличения емкости таблицы при превышении max_load_factor."""
    ht = HashTable()
    initial_capacity = ht._capacity

    # Добавляем элементы до превышения max_load_factor (0.9 по умолчанию)
    trigger_count = int(initial_capacity * ht.max_load_factor) + 1
    for i in range(trigger_count):
        ht[f'key_{i}'] = i

    assert ht._capacity > initial_capacity
    assert ht._capacity == initial_capacity * 2
    assert len(ht) == trigger_count
    # Проверяем, что данные не потерялись после рехеширования
    for i in range(trigger_count):
        assert ht[f'key_{i}'] == i


def test_rebuild_scale_down():
    """Тест уменьшения емкости таблицы при падении ниже min_load_factor."""
    ht = HashTable()
    # Сначала искусственно раздуваем таблицу
    for i in range(20):
        ht[f'key_{i}'] = i

    expanded_capacity = ht._capacity

    # Теперь удаляем элементы, чтобы вызвать уменьшение размера (min_load_factor по умолчанию 0.25)
    for i in range(19):
        del ht[f'key_{i}']

    assert ht._capacity < expanded_capacity
    assert ht._capacity == HASH_TABLE_INITIAL_CAPACITY
    assert len(ht) == 1


# --- 5. Тесты представлений (Views) ---


def test_items_view():
    """Тест представления элементов (items)."""
    ht = HashTable({'a': 1, 'b': 2})
    view = ht.items()
    assert isinstance(view, HashTableItemsView)
    assert len(view) == 2
    items_list = list(view)
    assert ('a', 1) in items_list
    assert ('b', 2) in items_list


def test_keys_view():
    """Тест представления ключей (keys)."""
    ht = HashTable({'a': 1, 'b': 2})
    view = ht.keys()
    assert isinstance(view, HashTableKeysView)
    assert len(view) == 2
    assert 'a' in view
    assert 'b' in view
    assert 'c' not in view
    assert set(view) == {'a', 'b'}


def test_values_view():
    """Тест представления значений (values)."""
    ht = HashTable({'a': 1, 'b': 2})
    view = ht.values()
    assert isinstance(view, HashTableValuesView)
    assert len(view) == 2
    assert 1 in view
    assert 2 in view
    assert 3 not in view
    assert sorted(view) == [1, 2]


# --- 6. Тесты метода update (singledispatchmethod) ---


def test_update_method_with_iterable():
    """Тест обновления таблицы через Iterable."""
    ht = HashTable({'a': 1})
    ht.update([('b', 2), ('c', 3)])
    assert len(ht) == 3
    assert ht['c'] == 3


def test_update_method_with_mapping():
    """Тест обновления таблицы через Mapping."""
    ht = HashTable({'a': 1})
    ht.update({'b': 2, 'a': 100})
    assert len(ht) == 2
    assert ht['a'] == 100
    assert ht['b'] == 2


def test_update_method_unsupported_type():
    """Тест вызова исключения при передаче неподдерживаемого типа в update."""
    ht = HashTable()
    with pytest.raises(NotImplementedError):
        ht.update(42)  # int не поддерживается


# --- 7. Тест строкового представления ---


def test_repr():
    """Тест строкового отображения объекта (__repr__)."""
    ht = HashTable()
    assert repr(ht) == '{}'
    ht['a'] = 1
    rep = repr(ht)
    assert rep == '{a: 1}'
