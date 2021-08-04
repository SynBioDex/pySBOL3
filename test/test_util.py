import unittest

import sbol3


class TestUtil(unittest.TestCase):

    def test_string_to_display_id(self):
        data = (
            ('foo', 'foo'),
            ('12', '_12'),
            # Handle non-ASCII
            ('世界', '世界'),
            ('Épée', 'Épée'),
            # convert special characters
            ('a b', 'a_b'),
            ('a-b', 'a_b'),
            ('a.b', 'a_b'),
            ('a:b', 'a_b'),
            ('a/b', 'a_b'),
            ('a\\b', 'a_b'),
            ('a -.:/\\b', 'a______b'),
            # convert multiple special characters
            ('this is-long.display/id', 'this_is_long_display_id'),
        )
        for input_str, expected in data:
            actual = sbol3.string_to_display_id(input_str)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
