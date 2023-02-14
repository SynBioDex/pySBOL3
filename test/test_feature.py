import unittest

import sbol3

class TestFeature(unittest.TestCase):
    
    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    # def test_create(self):
    #     sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
    #     display_id = 'feature1'
    #     feat = sbol3.feature(display_id)
    #     self.assertIsNotNone(feat)
    #     # self.assertEqual(display_id, feat.display_id)
    #     # self.assertIsNone(feat.roles)


    # def test_invalid(self):

    if __name__ == '__main__':
        unittest.main()