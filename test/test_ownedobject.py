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
                                name=con1_id)
        expected = posixpath.join(sbol3.get_homespace(), con1_id)
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

    def test_identity_set(self):
        # This test uses assignment instead of appending
        comp = sbol3.Component('c1', sbol3.SBO_DNA)
        con1_id = 'con1'
        con1 = sbol3.Constraint(sbol3.SBOL_REPLACES,
                                'http://example.com/fake1',
                                'http://example.com/fake2',
                                name=con1_id)
        expected = posixpath.join(sbol3.get_homespace(), con1_id)
        expected2 = posixpath.join(comp.identity, 'Constraint1')
        self.assertNotEqual(expected, expected2)
        self.assertEqual(expected, con1.identity)
        # Setting to list should cause the constraint's identity to change
        comp.constraints = [con1]
        self.assertEqual(expected2, con1.identity)

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

    # TODO: Write tests for adding via a slice
    #       comp.constraints[0:1] = sbol3.Constraint('foo')


if __name__ == '__main__':
    unittest.main()
