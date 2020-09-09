import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestSIPrefix(unittest.TestCase):

    def test_create(self):
        display_id = 'si_prefix'
        symbol = 'kilo'
        label = 'Kilo'
        factor = 1000
        prefix = sbol3.SIPrefix(display_id, symbol, label, factor)
        self.assertIsNotNone(prefix)
        self.assertEqual(symbol, prefix.symbol)
        self.assertEqual(label, prefix.label)
        self.assertAlmostEqual(float(factor), prefix.factor, 10)
        self.assertIsInstance(prefix.factor, float)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'measurement_entity',
                                 'measurement', 'measurement.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        uri = 'https://sbolstandard.org/examples/milli'
        si_prefix = doc.find(uri)
        self.assertIsNotNone(si_prefix)
        self.assertIsInstance(si_prefix, sbol3.SIPrefix)
        # TODO: The example is invalid because it has no 'symbol' property
        #       This test will fail when the test file gets updated
        self.assertIsNone(si_prefix.symbol)
        self.assertEqual('milli', si_prefix.label)
        self.assertCountEqual(['m1', 'm2'], si_prefix.alternative_symbols)
        self.assertCountEqual(['milli1', 'milli2'], si_prefix.alternative_labels)
        self.assertAlmostEqual(0.001, si_prefix.factor, 3)
        self.assertIsNotNone(si_prefix.long_comment)
        self.assertIsNotNone(si_prefix.description)
        self.assertIsNotNone(si_prefix.comment)


class TestBinaryPrefix(unittest.TestCase):

    def test_create(self):
        display_id = 'binary_prefix'
        symbol = 'kilo'
        label = 'Kilo'
        factor = 1000
        prefix = sbol3.BinaryPrefix(display_id, symbol, label, factor)
        self.assertIsNotNone(prefix)
        self.assertEqual(symbol, prefix.symbol)
        self.assertEqual(label, prefix.label)
        self.assertAlmostEqual(float(factor), prefix.factor, 10)
        self.assertIsInstance(prefix.factor, float)

    def test_read_from_file(self):
        # BinaryPrefix does not appear in any test files
        pass


if __name__ == '__main__':
    unittest.main()
