import unittest

import sbol3


class TestVariableFeature(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        vc = sbol3.VariableFeature(cardinality=sbol3.SBOL_ZERO_OR_MORE,
                                   variable=sbol3.PYSBOL3_MISSING)
        self.assertIsNotNone(vc)
        # Verify the correct default values
        self.assertEqual(sbol3.SBOL_ZERO_OR_MORE, vc.cardinality)
        self.assertEqual(sbol3.PYSBOL3_MISSING, vc.variable)
        self.assertEqual(sbol3.SBOL_VARIABLE_FEATURE, vc.type_uri)

    def test_invalid_create(self):
        my_cardinality = 'https://github.com/synbiodex/pysbol3#someNumber'
        vf = sbol3.VariableFeature(cardinality=my_cardinality,
                                   variable=sbol3.PYSBOL3_MISSING)
        report = vf.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

    def test_round_trip1(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/155
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc1 = sbol3.Document()
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        doc1.add(comp1)
        cd1 = sbol3.CombinatorialDerivation('cd1', comp1)
        self.assertEqual(comp1.identity, cd1.template)
        doc1.add(cd1)
        vf1 = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE,
                                    variable=sbol3.PYSBOL3_MISSING)
        cd1.variable_features.append(vf1)
        self.assertTrue(vf1.identity.startswith(cd1.identity))
        doc2 = sbol3.Document()
        doc2.read_string(doc1.write_string(sbol3.SORTED_NTRIPLES),
                         sbol3.SORTED_NTRIPLES)
        comp2 = doc2.find(comp1.identity)
        self.assertIsInstance(comp2, sbol3.Component)
        cd2 = doc2.find(cd1.identity)
        self.assertIsInstance(cd2, sbol3.CombinatorialDerivation)
        vf2 = doc2.find(vf1.identity)
        self.assertIsInstance(vf2, sbol3.VariableFeature)

    def test_round_trip2(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/159
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc1 = sbol3.Document()
        comp1 = sbol3.Component('comp1', sbol3.SBO_DNA)
        doc1.add(comp1)
        cd1 = sbol3.CombinatorialDerivation('cd1', comp1)
        self.assertEqual(comp1.identity, cd1.template)
        doc1.add(cd1)
        vf1 = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE,
                                    variable=sbol3.PYSBOL3_MISSING)
        hour = 'https://identifiers.org/ncit:C25529'
        m1 = sbol3.Measure(32, hour)
        vf1.variant_measures.append(m1)
        cd1.variable_features.append(vf1)
        self.assertTrue(vf1.identity.startswith(cd1.identity))
        # Ensure that Measure m1 is valid. The bug tested here was that it
        # had been assigned an invalid displayId.
        report = m1.validate()
        self.assertEqual(0, len(report.errors))

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        seq = sbol3.Sequence('seq1')
        test_loc = sbol3.EntireSequence(seq)
        variable_uri = 'https://example.org/variable'
        var_coll_uri = 'https://example.org/collection'
        var_feat1 = sbol3.VariableFeature(cardinality=sbol3.SBOL_ZERO_OR_MORE,
                                          variable=variable_uri,
                                          variant_collections=var_coll_uri)
        self.assertEqual([var_coll_uri], var_feat1.variant_collections)


if __name__ == '__main__':
    unittest.main()
