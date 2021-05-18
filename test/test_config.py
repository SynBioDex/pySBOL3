import unittest

import sbol3


class TestConfig(unittest.TestCase):

    # I wanted to have this in a base class but I couldn't get the
    # imports right. I kept getting "attempted relative import with
    # no known parent package".
    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_namespace(self):
        base_uri = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(base_uri)
        self.assertEqual(base_uri, sbol3.get_namespace())

        # Example from SBOL 3.0 Section 5.1 (page 12)
        # See issue #80
        base_uri = 'https://synbiohub.org'
        sbol3.set_namespace(base_uri)
        self.assertEqual(base_uri, sbol3.get_namespace())

    def test_no_namespace(self):
        # This test requires that no objects have been created without
        # a namespace set. The warning only triggers on the first such
        # creation. There is probably a way to reset the triggering of
        # warnings if we need that in the future.
        #
        # Make sure there is no default namespace
        self.assertEqual(None, sbol3.get_namespace())
        # Make sure creation without a namespace generates a warning
        display_id = 'c1'
        with self.assertWarns(UserWarning) as cm:
            c = sbol3.Component(display_id, sbol3.SBO_DNA)
        # We expect the warning to come from object.py. Update this if
        # the logic changes.
        self.assertIn('object.py', cm.filename)
        # We expect the default namespace to appear in the identity
        self.assertIn(sbol3.PYSBOL3_DEFAULT_NAMESPACE, c.identity)
        # We expect the default namespace at the beginning of the identity
        self.assertTrue(c.identity.startswith(sbol3.PYSBOL3_DEFAULT_NAMESPACE))
        # We expect the display_id to appear in the identity
        self.assertIn(display_id, c.identity)
        # We expect the display_id to be at the end of the identity
        self.assertTrue(c.identity.endswith(display_id))


if __name__ == '__main__':
    unittest.main()
