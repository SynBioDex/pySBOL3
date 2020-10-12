import unittest
import sbol3


class TestConfig(unittest.TestCase):

    # I wanted to have this in a base class but I couldn't get the
    # imports right. I kept getting "attempted relative import with
    # no known parent package".
    def setUp(self) -> None:
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

    def test_parse_class_name(self):
        # Test parsing with # delimiter in type URI
        c = sbol3.Component('c', sbol3.SBO_DNA)
        class_name = sbol3.config.parse_class_name(c.type_uri)
        self.assertEqual(class_name, 'Component')

        # Test parsing with # delimiter in type URI
        m = sbol3.Measure(0, 'dollars')
        class_name = sbol3.config.parse_class_name(m.type_uri)
        self.assertEqual(class_name, 'Measure')

        # Test failure with invalid type URI
        with self.assertRaises(ValueError):
            sbol3.config.parse_class_name('Component')


if __name__ == '__main__':
    unittest.main()
