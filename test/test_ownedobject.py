import posixpath
import unittest
import sbol3


class TestOwnedObject(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_identity_append(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        con1 = sbol3.Constraint(sbol3.SBOL_REPLACES,
                                'http://example.com/fake1',
                                'http://example.com/fake2')
        # The constraint's identity and display_id will be overwritten as
        # part of the append operation. SBOL Compliant URIs (identities)
        # use the class of the object and a counter to generate the
        # display_id.
        expected2 = posixpath.join(comp.identity, 'Constraint1')
        # Append should cause the constraint's identity to change
        comp.constraints.append(con1)
        self.assertEqual(expected2, con1.identity)

    def test_list_property_update_identity(self):
        # This test uses assignment instead of appending
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        con1 = sbol3.Constraint(sbol3.SBOL_REPLACES,
                                'http://example.com/fake1',
                                'http://example.com/fake2')
        expected2 = posixpath.join(comp.identity, 'Constraint1')
        # Setting to list should cause the constraint's identity to change
        comp.constraints = [con1]
        self.assertEqual(expected2, con1.identity)

    def test_singleton_property_update_identity(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        tl = sbol3.CustomTopLevel('foo', 'http://synbio.bbn.com/opil#MeasurementValue')
        tl.measure = sbol3.OwnedObject(tl, 'http://synbio.bbn.com/opil#measure', 0, 1)
        m = sbol3.Measure(10, 'liters')
        tl.measure = m
        expected = posixpath.join(tl.identity, 'Measure1')
        self.assertIsNotNone(tl.measure.identity)
        self.assertEqual(expected, tl.measure.identity)

    def test_add_multiple_children(self):
        # Test that the the display_id and identity are overwritten
        # properly when adding multiple child entities.
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        comp.constraints.append(sbol3.Constraint(sbol3.SBOL_REPLACES,
                                                 'http://example.com/fake1',
                                                 'http://example.com/fake2'))
        expected1 = posixpath.join(comp.identity, 'Constraint1')
        self.assertEqual(expected1, comp.constraints[0].identity)
        comp.constraints.append(sbol3.Constraint(sbol3.SBOL_REPLACES,
                                                 'http://example.com/fake1',
                                                 'http://example.com/fake2'))
        expected2 = posixpath.join(comp.identity, 'Constraint2')
        self.assertEqual(expected2, comp.constraints[1].identity)

    def test_identity_conflict2(self):
        # Test that the same display id will cause a validation
        # error when an item with the same display id is appended
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        constraints = [sbol3.Constraint(sbol3.SBOL_REPLACES,
                                        'http://example.com/fake1',
                                        'http://example.com/fake2'),
                       sbol3.Constraint(sbol3.SBOL_REPLACES,
                                        'http://example.com/fake1',
                                        'http://example.com/fake2')]
        comp.constraints = constraints
        expected1 = posixpath.join(comp.identity, 'Constraint1')
        self.assertEqual(expected1, comp.constraints[0].identity)
        expected2 = posixpath.join(comp.identity, 'Constraint2')
        self.assertEqual(expected2, comp.constraints[1].identity)

    def test_cascade_identity(self):
        # Test that updating identity of an owned object cascades
        # to child owned objects
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        seq = sbol3.Sequence('seq1')
        loc = sbol3.EntireSequence(seq)
        seq_feature = sbol3.SequenceFeature([loc])
        c1.features.append(seq_feature)
        self.assertIsNotNone(seq_feature.identity)
        # identity should cascade down to the location after it
        # is set on the sequence feature
        self.assertIsNotNone(loc.identity)

    def test_overwrite_identity(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        seq = sbol3.Sequence('seq1')
        loc = sbol3.EntireSequence(seq)
        seq_feature = sbol3.SequenceFeature([loc])
        c1.features.append(seq_feature)
        self.assertIsNotNone(seq_feature.identity)
        # identity should cascade down to the location after it
        # is set on the sequence feature
        self.assertIsNotNone(loc.identity)
        old_sf_identity = seq_feature.identity
        old_loc_identity = loc.identity
        c2 = sbol3.Component('c2', sbol3.SBO_DNA)
        # Try adding the same object to a different parent
        # This should cause an error because the object is
        # still parented by c1.
        # See https://github.com/SynBioDex/pySBOL3/issues/178
        with self.assertRaises(ValueError):
            c2.features.append(seq_feature)
        self.assertEqual(old_loc_identity, loc.identity)
        self.assertEqual(old_sf_identity, seq_feature.identity)

    def test_type_constraint(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('foo', sbol3.SBO_DNA)
        with self.assertRaises(TypeError):
            c.features = [sbol3.Range('https://example.com/fake', 1, 2)]
        self.assertEqual(c.features.type_constraint, sbol3.Feature)

    def test_set_document(self):
        # Ensure that document is set on child objects
        # See https://github.com/SynBioDex/pySBOL3/issues/176
        sbol3.set_namespace('https://bioprotocols.org/paml/primitives/')
        doc = sbol3.Document()
        c = sbol3.Component("scratch", sbol3.SBO_DNA)
        doc.add(c)
        lsc = sbol3.LocalSubComponent([sbol3.SBO_DNA])
        self.assertIsNone(lsc.document)
        c.features.append(lsc)
        self.assertIsNotNone(lsc.document)
        interaction = sbol3.Interaction([sbol3.SBO_DEGRADATION])
        c.interactions.append(interaction)
        self.assertEqual(doc, interaction.document)
        p = sbol3.Participation([sbol3.SBO_REACTANT], lsc)
        interaction.participations.append(p)
        self.assertEqual(doc, p.document)
        resolved_lsc = p.participant.lookup()
        self.assertEqual(lsc, resolved_lsc)
        self.assertEqual(lsc.identity, resolved_lsc.identity)

    # TODO: Write tests for adding via a slice
    #       comp.constraints[0:1] = sbol3.Constraint('foo')

    def test_compose_then_set_document(self):
        # Ensure that document is set on child objects
        # See https://github.com/SynBioDex/pySBOL3/issues/230
        sbol3.set_namespace('https://bioprotocols.org/paml/primitives/')
        c = sbol3.Component("scratch", sbol3.SBO_DNA)
        lsc = sbol3.LocalSubComponent([sbol3.SBO_DNA])
        self.assertIsNone(lsc.document)
        c.features.append(lsc)
        doc = sbol3.Document()
        doc.add(c)
        self.assertIsNotNone(lsc.document)
        self.assertEqual(doc, lsc.document)
        interaction = sbol3.Interaction([sbol3.SBO_DEGRADATION])
        p = sbol3.Participation([sbol3.SBO_REACTANT], lsc)
        interaction.participations.append(p)
        c.interactions.append(interaction)
        # Now that we've composed the objects, add them to the parent.
        # This should assign the document to all the objects in the hierarchy
        # See https://github.com/SynBioDex/pySBOL3/issues/230
        self.assertEqual(doc, interaction.document)
        self.assertEqual(doc, p.document)
        resolved_lsc = p.participant.lookup()
        self.assertEqual(lsc, resolved_lsc)
        self.assertEqual(lsc.identity, resolved_lsc.identity)


if __name__ == '__main__':
    unittest.main()
