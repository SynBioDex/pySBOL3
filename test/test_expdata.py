import unittest

import sbol3


class TestExperimentalData(unittest.TestCase):

    # This class could use some more tests. Not sure what else to put
    # here. There are not yet any examples in the SBOLTestSuite. And
    # the class doesn't have any properties of its own.

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'exp_data'
        exp_data = sbol3.ExperimentalData(display_id)
        self.assertIsNotNone(exp_data)
        self.assertEqual(display_id, exp_data.display_id)
        self.assertTrue(hasattr(exp_data, 'attachments'))
        self.assertEqual(sbol3.SBOL_EXPERIMENTAL_DATA, exp_data.type_uri)

    def test_create2(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'exp_data'
        c1 = sbol3.Component('c1', [sbol3.SBO_DNA])
        exp_data = sbol3.ExperimentalData(display_id, attachments=[c1])
        self.assertIsNotNone(exp_data)
        self.assertEqual(display_id, exp_data.display_id)
        self.assertTrue(hasattr(exp_data, 'attachments'))
        self.assertEqual(sbol3.SBOL_EXPERIMENTAL_DATA, exp_data.type_uri)
        self.assertCountEqual([c1.identity], exp_data.attachments)


if __name__ == '__main__':
    unittest.main()
