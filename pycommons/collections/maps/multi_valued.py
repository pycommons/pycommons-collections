from typing import TypeVar

from pycommons.collections.maps import IterableMap
from pycommons.collections.sets.ordered import OrderedSet

_K = TypeVar("_K")
_V = TypeVar("_V")


class MultiValuedMap(IterableMap[_K, OrderedSet[_V]]):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in self and isinstance(self.data[key], OrderedSet):
            self.data[key].add(value)
        elif key in self and not isinstance(self.data[key], OrderedSet):
            self.data[key] = OrderedSet((self.data[key], value))
        elif key not in self:
            self.data[key] = OrderedSet((value,))
