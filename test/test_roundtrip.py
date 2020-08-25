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

    def find_all_files(self, dirname: str):
        for item in os.listdir(dirname):
            item_path = os.path.join(dirname, item)
            if os.path.isdir(item_path):
                for f in self.find_all_files(item_path):
                    yield f
            elif os.path.isfile(item_path):
                yield item_path
            else:
                print(f'{item} is neither file nor directory')

    @staticmethod
    def rdf_type(filename: str):
        filename = os.path.basename(filename)
        if filename.endswith('.sbol'):
            filename = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        # drop the leading dot
        ext = ext[1:]
        # TODO: 7 of 8 RDF/XML files have default namespace problems
        #       See https://github.com/SynBioDex/SBOLTestSuite/issues/19
        # ext_map = {'ntriples': 'nt', 'rdfxml': 'xml', 'turtle': 'ttl'}
        ext_map = {'ntriples': 'nt', 'turtle': 'ttl'}
        if ext in ext_map:
            return ext_map[ext]
        else:
            return None

    def test_read_all(self):
        # In lieu of round tripping the files, just make sure we can
        # read them all.
        # This is intended as a temporary test until the library is
        # more complete.
        skip_files = ['BBa_F2620_PoPSReceiver.rdfxml.sbol',
                      'interface.rdfxml.sbol',
                      'collection.rdfxml.sbol',
                      'implementation.rdfxml.sbol',
                      # 'multicellular.turtle.sbol',
                      'multicellular.rdfxml.sbol',
                      # 'multicellular.ntriples.sbol',
                      'toggle_switch.rdfxml.sbol',
                      'multicellular_simple.rdfxml.sbol']
        for f in self.find_all_files(SBOL3_LOCATION):
            if os.path.basename(f) in skip_files:
                # print(f'Skipping {f}')
                continue
            rdf_type = self.rdf_type(f)
            if rdf_type is None:
                # Skip file types we don't know
                # print(f'Skipping {f} of type {rdf_type}')
                continue
            # print(f'Reading {f}')
            doc = sbol3.Document()
            doc.read(f, format=rdf_type)


if __name__ == '__main__':
    unittest.main()
