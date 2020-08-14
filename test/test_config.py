import unittest

import sbol3


class TestConfig(unittest.TestCase):

    # I wanted to have this in a base class but I couldn't get the
    # imports right. I kept getting "attempted relative import with
    # no known parent package".
    def setUp(self) -> None:
        sbol3.set_defaults()

    def test_homespace(self):
        base_uri = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_homespace(base_uri)
        self.assertEqual(base_uri, sbol3.get_homespace())


if __name__ == '__main__':
    unittest.main()
