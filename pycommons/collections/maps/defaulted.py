from typing import TypeVar, Generic, Any

from pycommons.collections.maps.iterable import IterableMap

_K = TypeVar("_K")
_V = TypeVar("_V")


class DefaultedMap(IterableMap[_K, _V], Generic[_K, _V]):
    def __init__(self, default_value: _V, *args: Any, **kwargs: Any):
        self._default_value = default_value
        super().__init__(*args, **kwargs)

    def __getitem__(self, item: _K) -> _V:
        return self.data.get(item, self._default_value)
