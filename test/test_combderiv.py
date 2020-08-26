import unittest

import sbol3


class TestCombinatorialDerivation(unittest.TestCase):

    def test_create(self):
        template = 'https://github.com/synbiodex/pysbol3/component'
        cd1 = sbol3.CombinatorialDerivation('cd1', template)
        self.assertEqual(template, cd1.template)
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        cd2 = sbol3.CombinatorialDerivation('cd2', comp1)
        self.assertEqual(comp1.identity, cd2.template)

    def test_invalid_strategy(self):
        # Test with invalid strategy
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        cd1 = sbol3.CombinatorialDerivation('cd1', comp1)
        cd1.strategy = sbol3.SBOL_INLINE
        with self.assertRaises(sbol3.ValidationError):
            cd1.validate()


if __name__ == '__main__':
    unittest.main()
