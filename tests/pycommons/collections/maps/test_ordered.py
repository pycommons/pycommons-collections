from unittest import TestCase

from pycommons.collections.maps import OrderedMap


class TestOrderedMap(TestCase):
    def test_ordered_map(self):
        ordered_map = OrderedMap()
        ordered_map["testKey1"] = "testValue1"
        ordered_map["testKey2"] = "testValue2"

        self.assertListEqual(["testKey1", "testKey2"], list(ordered_map.keys()))
        self.assertListEqual(["testValue1", "testValue2"], list(ordered_map.values()))

        self.assertEqual("{'testKey1': 'testValue1', 'testKey2': 'testValue2'}", repr(ordered_map))
