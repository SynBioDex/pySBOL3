import unittest

import sbol3


class TestLocalSubComponent(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        types = [sbol3.SBO_DNA]
        lsc = sbol3.LocalSubComponent(types)
        self.assertIsNotNone(lsc)
        self.assertEqual(types, lsc.types)
        self.assertEqual([], lsc.locations)

    def test_validation(self):
        types = []
        lsc = sbol3.LocalSubComponent(types)
        report = lsc.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))


if __name__ == '__main__':
    unittest.main()
