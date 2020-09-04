import unittest

import sbol3


class TestLocalSubComponent(unittest.TestCase):

    def test_create(self):
        display_id = 'local1'
        types = [sbol3.SBO_DNA]
        lsc = sbol3.LocalSubComponent(display_id, types)
        self.assertIsNotNone(lsc)
        self.assertEqual(types, lsc.types)
        self.assertEqual(display_id, lsc.display_id)
        self.assertEqual([], lsc.locations)

    def test_validation(self):
        display_id = 'local1'
        types = []
        with self.assertRaises(sbol3.ValidationError):
            sbol3.LocalSubComponent(display_id, types)


if __name__ == '__main__':
    unittest.main()
