import unittest

import sbol3


class TestSubComponent(unittest.TestCase):

    def test_create(self):
        sc = sbol3.SubComponent('sc1')
        self.assertIsNotNone(sc)
        # Verify the correct default values
        self.assertEqual(sbol3.PYSBOL3_MISSING, sc.instance_of)


if __name__ == '__main__':
    unittest.main()
