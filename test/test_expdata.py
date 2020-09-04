import unittest

import sbol3


class TestExperimentalData(unittest.TestCase):

    # This class could use some more tests. Not sure what else to put
    # here. There are not yet any examples in the SBOLTestSuite. And
    # the class doesn't have any properties of its own.

    def test_create(self):
        display_id = 'exp_data'
        exp_data = sbol3.ExperimentalData(display_id)
        self.assertIsNotNone(exp_data)
        self.assertEqual(display_id, exp_data.display_id)
        self.assertTrue(hasattr(exp_data, 'attachments'))


if __name__ == '__main__':
    unittest.main()
