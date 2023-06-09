from __future__ import annotations

from typing import TypeVar, Tuple, Generic, Any, Union

from pycommons.collections.maps.iterable import MapIterator
from pycommons.collections.maps.sized import BoundedMap

_K = TypeVar("_K")
_V = TypeVar("_V")


class UnmodifiableMapIterator(MapIterator[_K, _V], Generic[_K, _V]):
    def set_value(self, val: _V) -> _V:
        raise TypeError(f"Cannot modify values in a {self.__class__.__name__}")

    def __next__(self) -> UnmodifiableMapIterator[_K, _V]:
        _next = next(self._items_iterator)
        return UnmodifiableMapIterator(self._data, self._items_iterator, _next[0], _next[1])


class UnmodifiableMap(BoundedMap[_K, _V], Generic[_K, _V]):
    __POP_DEFAULT_VALUE = object()

    def is_full(self) -> bool:
        return True

    def max_size(self) -> int:
        return self._max_size

    def _allow_set_item(self, key: _K) -> bool:
        return self.__init and key is not None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.__init: bool = True
        super().__init__(*args, **kwargs)
        self._max_size = len(self.data)
        self.__init = False

    def __setitem__(self, key: _K, value: _V) -> None:
        if self._allow_set_item(key):
            return super().__setitem__(key, value)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def popitem(self) -> Tuple[_K, _V]:
        if self.__init:
            return super().popitem()
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def __delitem__(self, key: _K) -> None:
        if self.__init:
            return self.data.__delitem__(key)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def update(self, __m: Any, **kwargs: Any) -> None:  # type: ignore
        if self.__init:
            return self.data.update(__m, **kwargs)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def pop(self, __key: Any, value: Union[_V, Any] = __POP_DEFAULT_VALUE) -> _V:
        if self.__init:
            if value == self.__POP_DEFAULT_VALUE:
                return self.data.pop(__key)
            return self.data.pop(__key, value)
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def clear(self) -> None:
        if self.__init:
            return super().clear()
        raise TypeError(f"Cannot modify {self.__class__.__name__}")

    def items_iterator(self) -> MapIterator[_K, _V]:
        return UnmodifiableMapIterator(self.data, iter(self.data.items()))


class UnmodifiableLateInitMap(UnmodifiableMap[_K, _V], Generic[_K, _V]):
    def max_size(self) -> int:
        return len(self.data)

    def is_full(self) -> bool:
        return False

    def _allow_set_item(self, key: _K) -> bool:
        return super()._allow_set_item(key) or key not in self.data
