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
        cd1.strategy = sbol3.SO_FORWARD
        report = cd1.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

    def test_round_trip(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/156
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        cd1 = sbol3.CombinatorialDerivation('cd1', comp1)
        self.assertEqual(comp1.identity, cd1.template)
        doc1 = sbol3.Document()
        doc1.add(comp1)
        doc1.add(cd1)
        doc2 = sbol3.Document()
        doc2.read_string(doc1.write_string(sbol3.SORTED_NTRIPLES),
                         sbol3.SORTED_NTRIPLES)
        comp2 = doc2.find(comp1.identity)
        self.assertIsInstance(comp2, sbol3.Component)
        cd2 = doc2.find(cd1.identity)
        self.assertIsInstance(cd2, sbol3.CombinatorialDerivation)


if __name__ == '__main__':
    unittest.main()
