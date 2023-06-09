import collections
from typing import TypeVar

from pycommons.collections.maps.iterable import IterableMap

_K = TypeVar("_K")
_V = TypeVar("_V")


class OrderedMap(IterableMap[_K, _V]):
    def __init__(self) -> None:
        super().__init__()
        self.data = collections.OrderedDict()

    def __str__(self) -> str:
        _str_list = []
        for map_iterator in self:
            _str_list.append(f"{repr(map_iterator.key)}: {repr(map_iterator.value)}")

        return f"{{{', '.join(_str_list)}}}"
