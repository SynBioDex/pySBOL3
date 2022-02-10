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

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_type = sbol3.SBO_DNA
        seq = sbol3.Sequence('seq1')
        test_loc = sbol3.EntireSequence(seq)
        lsc = sbol3.LocalSubComponent(types=test_type,
                                      locations=test_loc)
        self.assertEqual([test_type], lsc.types)
        self.assertEqual([test_loc], lsc.locations)


if __name__ == '__main__':
    unittest.main()
