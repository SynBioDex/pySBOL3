import unittest

import sbol3


class TestSequenceFeature(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        es1 = sbol3.EntireSequence(sbol3.PYSBOL3_MISSING)
        locations = [es1]
        sf = sbol3.SequenceFeature(locations)
        self.assertEqual(locations, sf.locations)

    def test_validation(self):
        locations = []
        with self.assertRaises(sbol3.ValidationError):
            sbol3.SequenceFeature(locations)


if __name__ == '__main__':
    unittest.main()
