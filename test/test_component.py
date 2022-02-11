import os
import posixpath
import unittest
from collections.abc import Container

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestComponent(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_roles(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        self.assertListEqual([], list(c.roles))
        self.assertEqual([], c.roles)
        c.roles = [sbol3.SO_PROMOTER]
        # Make sure the underlying datatype did not get overwritten
        self.assertNotIsInstance(c.roles, list)
        self.assertIsInstance(c.roles, Container)
        self.assertIn(sbol3.SO_PROMOTER, c.roles)
        self.assertEqual([sbol3.SO_PROMOTER], c.roles)
        self.assertTrue(c.roles == [sbol3.SO_PROMOTER])
        self.assertTrue([sbol3.SO_PROMOTER] == c.roles)
        # Other list manipulations
        c.roles.append(sbol3.SO_CDS)
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_CDS], c.roles)
        self.assertEqual([sbol3.SO_CDS], c.roles[1:])
        c.roles[1:] = [sbol3.SO_RBS]
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_RBS], c.roles)
        self.assertEqual([sbol3.SO_RBS], c.roles[1:])

    def test_features(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/149
        # Note: this example was modified when fixing
        #       https://github.com/SynBioDex/pySBOL3/issues/178
        #       media_variable is unused in the original example so
        #       it has been commented out here

        media_template = sbol3.LocalSubComponent(types=[sbol3.SBO_FUNCTIONAL_ENTITY])
        media_template.name = 'media template'

        # variable_uri = 'https://github.com/synbiodex/pysbol3/variable'
        # media_variable = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE,
        #                                        variable=media_template)
        # media_variable.variable = media_template

        all_sample_templates = [media_template]
        sample_template_uri = 'https://sd2e.org/measurement_template'
        sample_template = sbol3.Component(identity=sample_template_uri,
                                          types=sbol3.SBO_FUNCTIONAL_ENTITY)
        sample_template.name = 'measurement template'
        sample_template.features = all_sample_templates
        self.assertEqual(1, len(sample_template.features))
        self.assertEqual(media_template.identity,
                         sample_template.features[0].identity)

    def test_type_validation(self):
        # Test the validation of types on owned object properties by
        # going behind the scenes to set a bad value
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        report = c1.validate()
        self.assertEqual(0, len(report))
        c1._owned_objects[sbol3.SBOL_FEATURES] = [sbol3.Interface(),
                                                  sbol3.Implementation('i1')
                                                  ]
        report = c1.validate()
        # Expecting 2 errors, one for each inappropriate value
        self.assertEqual(2, len(report))

    def test_cloning(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        new_identity = 'c2'
        c2 = c1.clone(new_identity)
        self.assertEqual(posixpath.join(sbol3.get_namespace(), new_identity),
                         c2.identity)

    def test_cloning_with_references(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        new_identity = 'c2'
        seq1 = sbol3.Sequence('s1')
        c1.sequences.append(seq1)
        c2 = c1.clone(new_identity)
        self.assertEqual(posixpath.join(sbol3.get_namespace(), new_identity),
                         c2.identity)
        self.assertListEqual(list(c1.sequences), list(c2.sequences))

    def test_cloning_with_children(self):
        # This test does not use `sbol3.set_namespace` as the other
        # cloning unit tests do. This is on purpose to verify that
        # cloning does not rely on the default namespace.
        doc = sbol3.Document()
        namespace = 'https://github.com/synbiodex/pysbol3'
        c1_identity = posixpath.join(namespace, 'c1')
        c2_identity = posixpath.join(namespace, 'c2')
        s1_identity = posixpath.join(namespace, 's1')
        c1 = sbol3.Component(c1_identity, sbol3.SBO_DNA)
        doc.add(c1)
        seq1 = sbol3.Sequence(s1_identity)
        doc.add(seq1)
        c1.sequences.append(seq1)
        sc1 = sbol3.SubComponent(c1)
        es1 = sbol3.EntireSequence(seq1)
        sc1.source_locations.append(es1)
        c1.features = [sc1]
        c2 = c1.clone(c2_identity)
        self.assertEqual(c2_identity, c2.identity)
        self.assertIsNone(c2.document)
        # Check on the SubComponent
        sc2 = c2.features[0]
        self.assertIsInstance(sc2, sbol3.SubComponent)
        self.assertNotEqual(sc1.identity, sc2.identity)
        self.assertTrue(sc2.identity.startswith(c2.identity))
        # Ensure that the reference was updated properly
        self.assertEqual(c2.identity, sc2.instance_of)
        self.assertIsNone(sc2.document)
        es2 = sc2.source_locations[0]
        self.assertIsInstance(es2, sbol3.EntireSequence)
        self.assertNotEqual(es1.identity, es2.identity)
        self.assertTrue(es2.identity.startswith(c2.identity))
        self.assertEqual(es1.sequence, es2.sequence)
        self.assertIsNone(es2.document)

    def test_cloning_references(self):
        # Verify that when we clone the constraint references
        # are in the namespace of the clone
        test_file = os.path.join(SBOL3_LOCATION, 'toggle_switch',
                                 'toggle_switch.nt')
        doc = sbol3.Document()
        doc.read(test_file)
        toggle_uri = 'https://sbolstandard.org/examples/toggle_switch'
        toggle = doc.find(toggle_uri)
        new_uri = 'https://github.com/synbiodex/pysbol3/toggle_switch'
        toggle_clone = toggle.clone(new_uri)
        self.assertNotEqual(toggle.identity, toggle_clone.identity)
        self.assertEqual(new_uri, toggle_clone.identity)
        doc2 = sbol3.Document()
        doc2.add(toggle_clone)
        self.assertEqual(len(toggle.constraints), len(toggle_clone.constraints))
        for i in range(len(toggle.constraints)):
            c = toggle.constraints[i]
            c_clone = toggle_clone.constraints[i]
            self.assertNotEqual(c.identity, c_clone.identity)
            s = c.subject.lookup()
            self.assertIsInstance(s, sbol3.ComponentReference)
            self.assertTrue(s.identity.startswith(toggle.identity))
            s_clone = c_clone.subject.lookup()
            self.assertIsInstance(s_clone, sbol3.ComponentReference)
            self.assertTrue(s_clone.identity.startswith(toggle_clone.identity))
            self.assertNotEqual(s.identity, s_clone.identity)
            self.assertEqual(s.refers_to, s_clone.refers_to)
            o = c.object.lookup()
            self.assertIsInstance(o, sbol3.ComponentReference)
            self.assertTrue(o.identity.startswith(toggle.identity))
            o_clone = c_clone.object.lookup()
            self.assertIsInstance(o_clone, sbol3.ComponentReference)
            self.assertTrue(o_clone.identity.startswith(toggle_clone.identity))
            self.assertNotEqual(o.identity, o_clone.identity)
            self.assertEqual(o.refers_to, o_clone.refers_to)

    def test_measures_initial_value(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        metre = 'http://www.ontology-of-units-of-measure.org/resource/om-2/metre'
        one_metre = sbol3.Measure(1, unit=metre)
        two_metres = sbol3.Measure(2, unit=metre)
        # Test passing a list of measures
        c1 = sbol3.Component('c1', types=[sbol3.SBO_DNA], measures=[one_metre, two_metres])
        self.assertListEqual([one_metre, two_metres], list(c1.measures))
        # test passing a singleton measure
        three_metres = sbol3.Measure(3, unit=metre)
        c2 = sbol3.Component('c2', types=[sbol3.SBO_DNA], measures=three_metres)
        self.assertListEqual([three_metres], list(c2.measures))

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        source_uri = 'https://example.org/source'
        derived_from_uri = 'https://example.org/derived_from'
        statute_mile = sbol3.OM_NS + 'mile-Statute'
        comp1_type = sbol3.SBO_DNA
        comp1_role = sbol3.SO_PROMOTER
        comp1_seq1 = sbol3.Sequence('seq1')
        comp1_model = sbol3.Model('model1',
                                  source=source_uri,
                                  language='https://example.org/language',
                                  framework='https://example.org/framework')
        comp1_attachment = sbol3.Attachment('att1', source=source_uri)
        comp1_measure = sbol3.Measure(value=26.2, unit=statute_mile)
        comp1_activity = sbol3.Activity('activity1')
        comp1 = sbol3.Component('comp1', types=comp1_type,
                                sequences=comp1_seq1, roles=comp1_role,
                                models=comp1_model,
                                attachments=comp1_attachment,
                                derived_from=derived_from_uri,
                                measures=comp1_measure,
                                generated_by=comp1_activity)
        self.assertEqual([comp1_type], comp1.types)
        self.assertEqual([comp1_seq1.identity], comp1.sequences)
        self.assertEqual([comp1_role], comp1.roles)
        self.assertEqual([comp1_model.identity], comp1.models)
        self.assertEqual([comp1_attachment.identity], comp1.attachments)
        self.assertEqual([derived_from_uri], comp1.derived_from)
        self.assertEqual([comp1_measure], comp1.measures)
        self.assertEqual([comp1_activity.identity], comp1.generated_by)


if __name__ == '__main__':
    unittest.main()
