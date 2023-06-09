from typing import Generic, TypeVar, Any

from pycommons.collections.maps.iterable import IterableMap
from pycommons.collections.maps.ordered import OrderedMap
from pycommons.lang.function import Predicate, BiPredicate

_K = TypeVar("_K")
_V = TypeVar("_V")


class PredicatedMap(IterableMap[_K, _V], Generic[_K, _V]):
    def __init__(
        self,
        key_predicate: Predicate[_K],
        value_predicate: Predicate[_V],
        *args: Any,
        **kwargs: Any
    ):
        self._key_predicate = key_predicate
        self._value_predicate = value_predicate
        super().__init__(*args, *kwargs)

    def __setitem__(self, key: _K, value: _V) -> None:
        self.validate_exceptionally(key, value)
        super().__setitem__(key, value)

    def validate(self, key: _K, value: _V) -> bool:
        return self.validate_key(key) and self.validate_value(value)

    def validate_exceptionally(self, key: _K, value: _V) -> None:
        if not self.validate_key(key):
            raise ValueError("Predicate not passing for the key passed")

        if not self.validate_value(value):
            raise ValueError("Predicate not passing for the value passed")

    def validate_key(self, key: _K) -> bool:
        return self._key_predicate.test(key)

    def validate_value(self, value: _V) -> bool:
        return self._value_predicate.test(value)


class PredicatedOrderedMap(PredicatedMap[_K, _V], OrderedMap[_K, _V], Generic[_K, _V]):
    def __init__(self, key_predicate: Predicate[_K], value_predicate: Predicate[_V]):
        PredicatedMap.__init__(self, key_predicate, value_predicate)
        OrderedMap.__init__(self)


class CompositePredicatedMap(IterableMap[_K, _V], Generic[_K, _V]):
    def __init__(self, predicate: BiPredicate[_K, _V], *args: Any, **kwargs: Any):
        self._predicate = predicate
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: _K, value: _V) -> None:
        self.validate_exceptionally(key, value)
        super().__setitem__(key, value)

    def validate(self, key: _K, value: _V) -> bool:
        return self._predicate.test(key, value)

    def validate_exceptionally(self, key: _K, value: _V) -> None:
        if not self.validate(key, value):
            raise ValueError("Predicate not passing for the key passed")
