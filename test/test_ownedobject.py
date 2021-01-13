import posixpath
import unittest
import sbol3


class TestOwnedObject(unittest.TestCase):

    def test_identity_append(self):
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        con1_id = 'con1'
        con1 = sbol3.Constraint(sbol3.SBOL_REPLACES,
                                'http://example.com/fake1',
                                'http://example.com/fake2',
                                identity=con1_id)
        expected = posixpath.join(sbol3.get_namespace(), con1_id)
        # The constraint's identity and display_id will be overwritten as
        # part of the append operation. SBOL Compliant URIs (identities)
        # use the class of the object and a counter to generate the
        # display_id.
        expected2 = posixpath.join(comp.identity, 'Constraint1')
        self.assertNotEqual(expected, expected2)
        self.assertEqual(expected, con1.identity)
        # Append should cause the constraint's identity to change
        comp.constraints.append(con1)
        self.assertEqual(expected2, con1.identity)

    def test_list_property_update_identity(self):
        # This test uses assignment instead of appending
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        con1_id = 'con1'
        con1 = sbol3.Constraint(sbol3.SBOL_REPLACES,
                                'http://example.com/fake1',
                                'http://example.com/fake2',
                                identity=con1_id)
        expected = posixpath.join(sbol3.get_namespace(), con1_id)
        expected2 = posixpath.join(comp.identity, 'Constraint1')
        self.assertNotEqual(expected, expected2)
        self.assertEqual(expected, con1.identity)
        # Setting to list should cause the constraint's identity to change
        comp.constraints = [con1]
        self.assertEqual(expected2, con1.identity)

    def test_singleton_property_update_identity(self):
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
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        con1_id = 'con1'
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
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        seq = sbol3.Sequence('seq1')
        loc = sbol3.EntireSequence(seq)
        seq_feature = sbol3.SequenceFeature([loc])
        c1.features.append(seq_feature)
        self.assertIsNotNone(seq_feature.identity)
        # identity should cascade down to the location after it
        # is set on the sequence feature
        self.assertIsNotNone(loc.identity)

    def test_type_constraint(self):
        c = sbol3.Component('foo', sbol3.SBO_DNA)
        with self.assertRaises(TypeError):
            c.features = [sbol3.Range('https://example.com/fake', 1, 2)]
        self.assertEqual(c.features.type_constraint, sbol3.Feature)

    # TODO: Write tests for adding via a slice
    #       comp.constraints[0:1] = sbol3.Constraint('foo')


if __name__ == '__main__':
    unittest.main()
