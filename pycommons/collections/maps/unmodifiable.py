from typing import TypeVar, Tuple, Generic

from pycommons.collections.maps import MapIterator
from pycommons.collections.maps.sized import BoundedMap

_K = TypeVar("_K")
_V = TypeVar("_V")


class UnmodifiableMapIterator(MapIterator[_K, _V], Generic[_K, _V]):

    def set_value(self, val: _V) -> _V:
        raise TypeError(f"Cannot modify values in a {self.__class__.__name__}")

    def __next__(self) -> MapIterator:
        _next = next(self._items_iterator)
        return UnmodifiableMapIterator(self._data, self._items_iterator, _next[0], _next[1])


class UnmodifiableMap(BoundedMap, Generic[_K, _V]):

    def is_full(self) -> bool:
        return True

    def max_size(self) -> int:
        return self._max_size

    def _allow_set_item(self, key: _K):
        return self.__init

    def __init__(self, *args, **kwargs):
        self.__init: bool = True
        super().__init__(*args, **kwargs)
        self._max_size = len(self.data)
        self.__init = False

    def __setitem__(self, key, value):
        if self._allow_set_item(key):
            return super().__setitem__(key, value)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def popitem(self) -> Tuple[_K, _V]:
        if self.__init:
            return super().popitem()
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def __delitem__(self, key):
        if self.__init:
            return super().__delitem__(key)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def update(self, __m, **kwargs: _V) -> None:
        if self.__init:
            return super().update(__m, **kwargs)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def pop(self, __key: _K) -> _V:
        if self.__init:
            return super().pop(__key)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def clear(self) -> None:
        if self.__init:
            return super().clear()
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def map_iterator(self) -> MapIterator:
        return UnmodifiableMapIterator(self.data, iter(self.data.items()))


class UnmodifiableLateInitMap(UnmodifiableMap):

    def max_size(self) -> int:
        return len(self.data)

    def is_full(self) -> bool:
        return False

    def _allow_set_item(self, key: _K):
        return super()._allow_set_item(key) or key not in self.data
