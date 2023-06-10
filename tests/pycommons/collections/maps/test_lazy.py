from unittest import TestCase

from pycommons.lang.container.integer import IntegerContainer
from pycommons.lang.function import Function

from pycommons.collections.maps import LazyMap, LazyOrderedMap


class TestLazyMap(TestCase):
    def test_lazy_map(self):
        container = IntegerContainer()
        lazy_map: LazyMap[str, int] = LazyMap(Function.of(lambda k: container.add_and_get(2)))

        self.assertEqual(2, lazy_map["key1"])
        self.assertEqual(4, lazy_map["key2"])
        self.assertEqual(6, lazy_map["key3"])
        self.assertEqual(6, lazy_map["key3"])


class TestLazyOrderedMap(TestCase):
    def test_lazy_map(self):
        container = IntegerContainer()
        lazy_ordered_map: LazyMap[str, int] = LazyOrderedMap(
            Function.of(lambda k: container.add_and_get(2))
        )

        self.assertEqual(2, lazy_ordered_map["key1"])
        self.assertEqual(4, lazy_ordered_map["key2"])
        self.assertEqual(6, lazy_ordered_map["key3"])
        self.assertEqual(8, lazy_ordered_map["key0"])

        self.assertListEqual(["key1", "key2", "key3", "key0"], list(lazy_ordered_map.keys()))
        self.assertListEqual([2, 4, 6, 8], list(lazy_ordered_map.values()))
