import unittest

import sbol3


class TestUtil(unittest.TestCase):

    def test_string_to_display_id(self):
        data = (
            ('foo', 'foo'),
            ('12', '_12'),
            ('世界', '世界'),  # Is this ok?
            ('Épée', 'Épée'),  # Is this ok?
            ('a:b', 'a_COLONb'),
        )
        for input_str, actual in data:
            self.assertEqual(actual, sbol3.string_to_display_id(input_str))


if __name__ == '__main__':
    unittest.main()
