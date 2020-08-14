import posixpath
import unittest

import rdflib

import sbol3


class TestIdentified(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def test_display_id(self):
        # self.assertEqual(None, sbol3.get_homespace())
        c1_display_id = 'c1'
        c = sbol3.Component(c1_display_id)
        self.assertEqual(c1_display_id, c.display_id)
        self.assertIsInstance(c.display_id, str)
        display_id = 'my_component'
        # Ensure that displayId cannot be set
        with self.assertRaises(AttributeError):
            c.display_id = display_id
        # Should still have the old value
        self.assertEqual(c1_display_id, c.display_id)
        # Under the covers
        self.assertIsInstance(c.properties[sbol3.SBOL_DISPLAY_ID][0],
                              rdflib.Literal)

    def test_identity_display_id(self):
        # Test setting of display_id
        #   * Test by passing display_id to constructor
        #   * Test by having display_id deduced from identity
        c1_display_id = 'c1'
        c1_identity = posixpath.join(sbol3.get_homespace(), c1_display_id)
        c1 = sbol3.Component(c1_display_id)
        self.assertEqual(c1_display_id, c1.display_id)
        self.assertEqual(c1_identity, c1.identity)
        # Now test identity and display_id from a URL-type URI
        c2_display_id = 'c2'
        c2_identity = posixpath.join(sbol3.get_homespace(), c2_display_id)
        c2 = sbol3.Component(c2_identity)
        self.assertEqual(c2_display_id, c2.display_id)
        self.assertEqual(c2_identity, c2.identity)


if __name__ == '__main__':
    unittest.main()
