from __future__ import annotations

from collections import UserDict
from collections.abc import Iterator
from typing import TypeVar, Dict, Generic

_K = TypeVar("_K")
_V = TypeVar("_V")


class MapIterator(Iterator, Generic[_K, _V]):

    def __init__(self, data: Dict[_K, _V], items_iterator: Iterator, current_key=None, current_value=None):
        self._data = data
        self._items_iterator: Iterator = items_iterator
        self._current_key = current_key
        self._current_value = current_value

    def get_key(self) -> _K:
        return self.key

    def get_value(self) -> _K:
        return self.value

    def set_value(self, val: _V) -> _V:
        _prev_val = self._current_value
        self._current_value = val
        self._data[self._current_key] = self._current_value
        return _prev_val

    @property
    def key(self) -> _K:
        return self._current_key

    @property
    def value(self) -> _V:
        return self._current_value

    @value.setter
    def value(self, val: _V):
        self.set_value(val)

    def __next__(self) -> MapIterator:
        _next = next(self._items_iterator)
        return MapIterator(self._data, self._items_iterator, _next[0], _next[1])


class IterableMap(UserDict, Generic[_K, _V]):

    def map_iterator(self) -> MapIterator:
        return MapIterator(self.data, iter(self.data.items()))

    def __iter__(self) -> MapIterator:
        return self.map_iterator()
