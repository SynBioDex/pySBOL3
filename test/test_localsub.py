import unittest

import sbol3


class TestLocalSubComponent(unittest.TestCase):

    def test_create(self):
        types = [sbol3.SBO_DNA]
        lsc = sbol3.LocalSubComponent(types)
        self.assertIsNotNone(lsc)
        self.assertEqual(types, lsc.types)
        self.assertEqual([], lsc.locations)

    def test_validation(self):
        types = []
        with self.assertRaises(sbol3.ValidationError):
            sbol3.LocalSubComponent(types)


if __name__ == '__main__':
    unittest.main()
