from unittest import TestCase

from pycommons.collections.maps import DefaultedMap


class TestDefaultedMap(TestCase):
    def test_defaulted_map(self):
        defaulted_map: DefaultedMap[str, str] = DefaultedMap("default", {"testKey1": "testValue2"})
        self.assertEqual("testValue2", defaulted_map["testKey1"])
        self.assertEqual("default", defaulted_map["unknownKey"])
