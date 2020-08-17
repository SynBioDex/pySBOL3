import posixpath
import unittest

import sbol3


class TestOwnedObject(unittest.TestCase):

    def test_identity_append(self):
        comp = sbol3.Component('c1')
        con1_id = 'con1'
        con1 = sbol3.Constraint(con1_id)
        expected = posixpath.join(sbol3.get_homespace(), con1_id)
        expected2 = posixpath.join(comp.identity, con1_id)
        self.assertNotEqual(expected, expected2)
        self.assertEqual(expected, con1.identity)
        # Append should cause the constraint's identity to change
        comp.constraints.append(con1)
        self.assertEqual(expected2, con1.identity)

    def test_identity_set(self):
        comp = sbol3.Component('c1')
        con1_id = 'con1'
        con1 = sbol3.Constraint(con1_id)
        expected = posixpath.join(sbol3.get_homespace(), con1_id)
        expected2 = posixpath.join(comp.identity, con1_id)
        self.assertNotEqual(expected, expected2)
        self.assertEqual(expected, con1.identity)
        # Append should cause the constraint's identity to change
        comp.constraints = [con1]
        self.assertEqual(expected2, con1.identity)

    def test_identity_conflict(self):
        # Test that the same display id will cause a validation
        # error when an item with the same display id is appended
        comp = sbol3.Component('c1')
        con1_id = 'con1'
        comp.constraints.append(sbol3.Constraint(con1_id))
        with self.assertRaises(sbol3.ValidationError):
            comp.constraints.append(sbol3.Constraint(con1_id))

    def test_identity_conflict2(self):
        # Test that the same display id will cause a validation
        # error when an item with the same display id is appended
        comp = sbol3.Component('c1')
        con1_id = 'con1'
        constraints = [sbol3.Constraint(con1_id), sbol3.Constraint(con1_id)]
        with self.assertRaises(sbol3.ValidationError):
            comp.constraints = constraints

    # TODO: Write tests for adding via a slice
    #       comp.constraints[0:1] = sbol3.Constraint('foo')


if __name__ == '__main__':
    unittest.main()
