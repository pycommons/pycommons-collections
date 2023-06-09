import abc
from typing import TypeVar, Generic

from pycommons.collections.maps.iterable import IterableMap

_K = TypeVar("_K")
_V = TypeVar("_V")


class BoundedMap(IterableMap, abc.ABC, Generic[_K, _V]):

    @abc.abstractmethod
    def is_full(self) -> bool: ...

    @abc.abstractmethod
    def max_size(self) -> int: ...


class FixedSizeMap(BoundedMap, Generic[_K, _V]):

    def is_full(self) -> bool:
        return len(self) == self._max_size - 1

    def max_size(self) -> int:
        return self._max_size

    def __init__(self, size: int, *args, **kwargs):
        self._max_size: int = size
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if len(self.data) == self._max_size:
            raise OverflowError(f"Size breached for {self.__class__.__name__}(max_size={self.max_size()})")
        super().__setitem__(key, value)


class SingletonMap(FixedSizeMap, Generic[_K, _V]):

    def __init__(self, *args, **kwargs):
        super().__init__(1, *args, **kwargs)
