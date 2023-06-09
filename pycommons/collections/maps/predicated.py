from typing import Generic, TypeVar

from pycommons.collections.maps import IterableMap, OrderedMap
from pycommons.lang.function import Predicate

_K = TypeVar("_K")
_V = TypeVar("_V")


class PredicatedMap(IterableMap[_K, _V], Generic[_K, _V]):

    def __init__(self, key_predicate: Predicate, value_predicate: Predicate, *args, **kwargs):
        self._key_predicate = key_predicate
        self._value_predicate = value_predicate
        super().__init__(*args, *kwargs)

    def __setitem__(self, key: _K, value: _V):
        self.validate_exceptionally(key, value)
        super().__setitem__(key, value)

    def validate(self, key: _K, value: _V) -> bool:
        return self.validate_key(key) and self.validate_value(value)

    def validate_exceptionally(self, key: _K, value: _V):
        if not self.validate_key(key):
            raise ValueError("Predicate not passing for the key passed")

        if not self.validate_value(value):
            raise ValueError("Predicate not passing for the value passed")

    def validate_key(self, key: _K):
        return self._key_predicate.test(key)

    def validate_value(self, value: _V):
        return self._value_predicate.test(value)


class PredicateOrderedMap(PredicatedMap, OrderedMap, Generic[_K, _V]):

    def __init__(self, key_predicate: Predicate[_K], value_predicate: Predicate[_V]):
        PredicatedMap.__init__(self, key_predicate, value_predicate)
        OrderedMap.__init__(self)
