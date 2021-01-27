import unittest

import sbol3


class TestCombinatorialDerivation(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        template = 'https://github.com/synbiodex/pysbol3/component'
        cd1 = sbol3.CombinatorialDerivation('cd1', template)
        self.assertEqual(template, cd1.template)
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        cd2 = sbol3.CombinatorialDerivation('cd2', comp1)
        self.assertEqual(comp1.identity, cd2.template)

    def test_invalid_strategy(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Test with invalid strategy
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        cd1 = sbol3.CombinatorialDerivation('cd1', comp1)
        cd1.strategy = sbol3.SBOL_INLINE
        with self.assertRaises(sbol3.ValidationError):
            cd1.validate()


if __name__ == '__main__':
    unittest.main()
