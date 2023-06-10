from unittest import TestCase

from pycommons.collections.maps import MultiValuedMap


class TestMultiValuedMap(TestCase):
    def test_multi_valued_map(self):
        multi_valued_map = MultiValuedMap({"testKey1": "testValue11"})
        self.assertTrue("testValue11" in multi_valued_map["testKey1"])

        multi_valued_map["testKey1"] = "testValue12"

        self.assertEqual(2, len(multi_valued_map["testKey1"]))
        self.assertTrue("testValue11" in multi_valued_map["testKey1"])
        self.assertTrue("testValue12" in multi_valued_map["testKey1"])
