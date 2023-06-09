import typing
from typing import TypeVar, Any, Generic

from pycommons.collections.maps.iterable import IterableMap
from pycommons.collections.sets.ordered import OrderedSet

_K = TypeVar("_K")
_V = TypeVar("_V")


class MultiValuedMap(IterableMap[_K, OrderedSet[_V]], Generic[_K, _V]):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: _K, value: _V) -> None:
        if key in self and isinstance(self.data[key], OrderedSet):
            self.data[key].add(value)
        elif key in self and not isinstance(self.data[key], OrderedSet):
            self.data[key] = OrderedSet((typing.cast(_V, self.data[key]), value))
        elif key not in self:
            self.data[key] = OrderedSet((value,))
