import unittest

import sbol3


class TestSequenceFeature(unittest.TestCase):

    def test_create(self):
        display_id = 'seqfeat1'
        es1 = sbol3.EntireSequence('es1')
        locations = [es1]
        sf = sbol3.SequenceFeature(display_id, locations)
        self.assertEqual(display_id, sf.display_id)
        self.assertEqual(locations, sf.locations)

    def test_validation(self):
        display_id = 'seqfeat1'
        locations = []
        with self.assertRaises(sbol3.ValidationError):
            sbol3.SequenceFeature(display_id, locations)


if __name__ == '__main__':
    unittest.main()
