import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestRange(unittest.TestCase):

    def test_creation(self):
        start = 1
        end = 10
        r = sbol3.Range('r1', start, end)
        self.assertIsNotNone(r)
        self.assertEqual(start, r.start)
        self.assertEqual(end, r.end)

    def test_invalid_create(self):
        start = 0
        end = 10
        with self.assertRaises(sbol3.ValidationError):
            sbol3.Range('r1', start, end)
        start = 1
        end = 0
        with self.assertRaises(sbol3.ValidationError):
            sbol3.Range('r1', start, end)
        # end must be >= start
        start = 10
        end = 9
        with self.assertRaises(sbol3.ValidationError):
            sbol3.Range('r1', start, end)
        start = 7
        end = 7
        r = sbol3.Range('r1', start, end)
        self.assertEqual(start, r.start)
        self.assertEqual(end, r.end)


if __name__ == '__main__':
    unittest.main()
