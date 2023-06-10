from unittest import TestCase

from pycommons.collections.maps import FixedSizeMap, SingletonMap


class FixedSizeMapTest(TestCase):
    def test_fixed_size_map(self):
        fixed_size_map: FixedSizeMap[str, str] = FixedSizeMap(
            3,
            {
                "testKey1": "testValue1",
                "testKey2": "testValue2",
            },
        )

        self.assertEqual(2, len(fixed_size_map))
        self.assertFalse(fixed_size_map.is_full())
        fixed_size_map["testKey3"] = "testValue3"

        self.assertEqual(3, fixed_size_map.size())
        self.assertEqual(3, fixed_size_map.max_size())
        self.assertTrue(fixed_size_map.is_full())

        with self.assertRaises(OverflowError):
            fixed_size_map["testKey4"] = "testValue4"


class SingletonMapTest(TestCase):
    def test_fixed_size_map(self):
        fixed_size_map: SingletonMap[str, str] = SingletonMap({"testKey1": "testValue1"})
        self.assertEqual(1, len(fixed_size_map))
        with self.assertRaises(OverflowError):
            fixed_size_map["testKey2"] = "testValue2"
