import unittest

import sbol3


class TestVariableComponent(unittest.TestCase):

    def test_create(self):
        vc = sbol3.VariableFeature()
        self.assertIsNotNone(vc)
        # Verify the correct default values
        self.assertEqual(sbol3.SBOL_ZERO_OR_MORE, vc.cardinality)
        self.assertEqual(sbol3.PYSBOL3_MISSING, vc.variable)

    def test_invalid_create(self):
        my_cardinality = 'https://github.com/synbiodex/pysbol3#someNumber'
        with self.assertRaises(sbol3.ValidationError):
            vc = sbol3.VariableFeature(cardinality=my_cardinality)


if __name__ == '__main__':
    unittest.main()
