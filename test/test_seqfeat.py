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
        sf = sbol3.SequenceFeature(locations)
        report = sf.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

    def test_recursive_validation(self):
        # Test that the owned object, in this case the Range,
        # is also validated when the SequenceFeature is validated.
        seq_uri = 'https://github.com/synbiodex/pysbol3/sequence'
        start = 10
        end = 1
        r = sbol3.Range(seq_uri, start, end)
        report = r.validate()
        # end < start is a validation error
        self.assertEqual(1, len(report.errors))
        sf = sbol3.SequenceFeature([r])
        report = sf.validate()
        # We should find the validation issue in the owned
        # object (the range).
        self.assertEqual(1, len(report.errors))

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        seq = sbol3.Sequence('seq1')
        test_loc = sbol3.EntireSequence(seq)
        seq_feat1 = sbol3.SequenceFeature(locations=test_loc)
        self.assertEqual([test_loc], seq_feat1.locations)


if __name__ == '__main__':
    unittest.main()
