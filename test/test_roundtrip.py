import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestRoundTrip(unittest.TestCase):

    def test_BBa_F2620_PoPSReceiver(self):
        sbol_path = os.path.join(SBOL3_LOCATION, 'BBa_F2620_PoPSReceiver',
                                 'BBa_F2620_PoPSReceiver.turtle.sbol')
        doc = sbol3.Document()
        doc.read(sbol_path, 'turtle')

        # All of this below is because we don't yet have Document.find().
        # When we do have Document.find() we should be able to do this:
        #
        # range_uri = 'https://synbiohub.org/public/igem/BBa_F2620/subcomponent_3/location_1'
        # range1 = doc.find(range_uri)

        comp_uri = 'https://synbiohub.org/public/igem/BBa_F2620'
        comp = doc.find(comp_uri)
        self.assertIsNotNone(comp)
        self.assertIsInstance(comp, sbol3.Component)
        self.assertEqual(7, len(comp.features))
        sub3 = None
        for feature in comp.features:
            if feature.display_id == 'subcomponent_3':
                sub3 = feature
                break
        self.assertIsNotNone(sub3)
        self.assertIsInstance(sub3, sbol3.SubComponent)
        range1 = None
        for loc in sub3.locations:
            if loc.display_id == 'location_1':
                range1 = loc
                break
        self.assertIsNotNone(range1)
        self.assertEqual(55, range1.start)
        self.assertEqual(108, range1.end)


if __name__ == '__main__':
    unittest.main()
