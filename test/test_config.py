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
        # Make sure there is no default namespace
        self.assertEqual(None, sbol3.get_namespace())
        # Make sure that creating an object with a display_id
        # and no default namespace raises an exception
        with self.assertRaises(sbol3.NamespaceError):
            c = sbol3.Component('c1', sbol3.SBO_DNA)


if __name__ == '__main__':
    unittest.main()
