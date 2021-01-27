import unittest

import sbol3
# Reach behind the curtain to test non-public function(s)
from sbol3.utils import parse_class_name


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_parse_class_name(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Test parsing with # delimiter in type URI
        c = sbol3.Component('c', sbol3.SBO_DNA)
        class_name = parse_class_name(c.type_uri)
        self.assertEqual(class_name, 'Component')

        # Test parsing with # delimiter in type URI
        m = sbol3.Measure(0, 'dollars')
        class_name = parse_class_name(m.type_uri)
        self.assertEqual(class_name, 'Measure')

        # Test failure with invalid type URI
        with self.assertRaises(ValueError):
            parse_class_name('Component')


if __name__ == '__main__':
    unittest.main()
