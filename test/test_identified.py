import unittest

import rdflib

import sbol3


class TestIdentified(unittest.TestCase):

    def test_display_id(self):
        c = sbol3.Component()
        self.assertEqual(None, c.display_id)
        display_id = 'my_component'
        c.display_id = display_id
        self.assertEqual(display_id, c.display_id)
        self.assertIsInstance(c.display_id, str)
        with self.assertRaises(TypeError):
            c.display_id = 32
        # Should still have the old value
        self.assertEqual(display_id, c.display_id)
        # Under the covers
        self.assertIsInstance(c.properties[sbol3.SBOL_DISPLAY_ID][0],
                              rdflib.Literal)
