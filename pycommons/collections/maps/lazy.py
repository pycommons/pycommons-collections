from typing import TypeVar, Generic

from pycommons.collections.maps.iterable import IterableMap
from pycommons.collections.maps.ordered import OrderedMap
from pycommons.lang.function import Function

_K = TypeVar("_K")
_V = TypeVar("_V")


class LazyMap(IterableMap[_K, _V], Generic[_K, _V]):

    def __init__(self, factory: Function[_K, _V], *args, **kwargs):
        self._factory = factory
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        if item not in self.data:
            self.data[item] = self._factory.apply(item)

        return self.data[item]


class LazyOrderedMap(LazyMap, OrderedMap, Generic[_K, _V]):

    def __init__(self, factory: Function[_K, _V]):
        LazyMap.__init__(self, factory)
        OrderedMap.__init__(self)
