from __future__ import annotations

import dataclasses
import typing
from collections import UserDict  # pylint: disable=E0611
from typing import Iterator, KeysView, ValuesView
from typing import TypeVar, Dict, Generic, Optional

_K = TypeVar("_K")
_V = TypeVar("_V")


@dataclasses.dataclass
class MapItem(Generic[_K, _V]):
    key: _K
    value: _V


class ItemsIterator(Iterator["ItemsIterator[_K, _V]"], Generic[_K, _V]):
    def __init__(
        self,
        data: Dict[_K, _V],
        items_iterator: Iterator[typing.Tuple[_K, _V]],
        current_key: Optional[_K] = None,
        current_value: Optional[_V] = None,
    ):
        self._data = data
        self._items_iterator: Iterator[typing.Tuple[_K, _V]] = items_iterator
        self._current_key: Optional[_K] = current_key
        self._current_value: Optional[_V] = current_value

    def get_key(self) -> _K:
        return self.key

    def get_value(self) -> _V:
        return self.value

    def get_item(self) -> MapItem[_K, _V]:
        return MapItem(self.key, self.value)

    def set_value(self, val: _V) -> _V:
        _prev_val = self._current_value
        self._current_value = val
        self._data[typing.cast(_K, self._current_key)] = self._current_value
        return typing.cast(_V, _prev_val)

    @property
    def key(self) -> _K:
        return typing.cast(_K, self._current_key)

    @property
    def value(self) -> _V:
        return typing.cast(_V, self._current_value)

    @value.setter
    def value(self, val: _V) -> None:
        self.set_value(val)

    def __next__(self) -> ItemsIterator[_K, _V]:
        _next = next(self._items_iterator)
        return ItemsIterator(self._data, self._items_iterator, _next[0], _next[1])


class IterableMap(UserDict, Generic[_K, _V]):  # type: ignore
    data: Dict[_K, _V]

    def __iter__(self) -> ItemsIterator[_K, _V]:
        return self.items_iterator()

    def items_iterator(self) -> ItemsIterator[_K, _V]:
        return ItemsIterator(self.data, iter(self.data.items()))

    def keys(self) -> typing.KeysView[_K]:
        return KeysView(self.data)

    def values(self) -> ValuesView[_V]:
        return ValuesView(self.data)

    def keys_iterator(self) -> Iterator[_K]:
        return iter(self.data.keys())

    def values_iterator(self) -> Iterator[_V]:
        return iter(self.values())

    def is_empty(self) -> bool:
        return self.size() == 0

    def size(self) -> int:
        return len(self.data)

    def contains_value(self, value: _V) -> bool:
        for item in self:
            if value == item.value:
                return True
        return False

    def contains_key(self, key: _K) -> bool:
        return key in self.data
