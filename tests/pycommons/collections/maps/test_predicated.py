import typing
from unittest import TestCase

from pycommons.collections.maps import ItemsIterator
from pycommons.collections.maps.predicated import (
    PredicatedMap,
    CompositePredicatedMap,
    PredicatedOrderedMap,
)
from pycommons.lang.function import Predicate, BiPredicate


class TestPredicatedMap(TestCase):
    def test_predicated_map(self):
        key_predicate: Predicate[str] = Predicate.of(
            lambda s: typing.cast(str, s).startswith("testKey")
        )
        value_predicate: Predicate[int] = Predicate.of(lambda i: i % 2 == 0)

        predicated_map: PredicatedMap[str, int] = PredicatedMap(
            key_predicate, value_predicate, {"testKey1": 2, "testKey2": 4}
        )

        self.assertFalse(predicated_map.validate("unknown", 8))
        with self.assertRaises(ValueError):
            predicated_map["unknown"] = 6

        self.assertFalse(predicated_map.validate("testKey3", 7))
        with self.assertRaises(ValueError):
            predicated_map["testKey3"] = 7


class TestPredicatedOrderedMap(TestCase):
    def test_predicated_ordered_map(self):
        key_predicate: Predicate[str] = Predicate.of(
            lambda s: typing.cast(str, s).startswith("testKey")
        )
        value_predicate: Predicate[int] = Predicate.of(lambda i: i % 2 == 0)

        predicated_map: PredicatedMap[str, int] = PredicatedOrderedMap(
            key_predicate, value_predicate
        )
        predicated_map["testKey1"] = 2
        predicated_map["testKey2"] = 4

        self.assertEqual(2, predicated_map.size())

        items_iterator = predicated_map.items_iterator()
        item1: ItemsIterator[str, int] = next(items_iterator)
        self.assertEqual("testKey1", item1.key)
        self.assertEqual(2, item1.value)

        item2: ItemsIterator = next(items_iterator)
        self.assertEqual("testKey2", item2.key)
        self.assertEqual(4, item2.value)


class TestCompositePredicatedMap(TestCase):
    def test_predicated_map(self):
        def _predicate(key: str, val: int):
            return key.startswith("testKey") and val % 2 == 0

        predicated_map: CompositePredicatedMap[str, int] = CompositePredicatedMap(
            BiPredicate.of(_predicate), {"testKey1": 2, "testKey2": 4}
        )

        self.assertFalse(predicated_map.validate("unknown", 8))
        with self.assertRaises(ValueError):
            predicated_map["unknown"] = 6

        self.assertFalse(predicated_map.validate("testKey3", 7))
        with self.assertRaises(ValueError):
            predicated_map["testKey3"] = 7
