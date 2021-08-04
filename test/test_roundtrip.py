import logging
import os
import shutil
import tempfile
import unittest

import rdflib
import rdflib.compare

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL_TEST_SUITE = os.path.join(MODULE_LOCATION, 'SBOLTestSuite')
SBOL3_LOCATION = os.path.join(SBOL_TEST_SUITE, 'SBOL3')
TEST_RESOURCE_DIR = os.path.join(MODULE_LOCATION, 'resources')

DEBUG_ENV_VAR = 'SBOL_TEST_DEBUG'


class TestRoundTrip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Skip reading these files
        # No files are skipped at this time. All SBOLTestSuite files can
        # be read.
        cls.skip_reading = [
        ]
        # Skip round tripping these files
        cls.skip_round_trip = [
        ]
        # Skip validating these files
        cls.skip_validation = [
        ]

    def setUp(self):
        sbol3.set_defaults()
        # Create temp directory
        self.temp_out_dir = tempfile.mkdtemp()
        self.logger = logging.getLogger('sbol3.test')
        if not self.logger.hasHandlers():
            logging.basicConfig()
        if DEBUG_ENV_VAR in os.environ:
            self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        # Remove directory after the test
        if self.temp_out_dir:
            shutil.rmtree(self.temp_out_dir)
            self.temp_out_dir = None
        sbol3.set_defaults()

    def test_BBa_F2620_PoPSReceiver(self):
        sbol_path = os.path.join(SBOL3_LOCATION, 'BBa_F2620_PoPSReceiver',
                                 'BBa_F2620_PoPSReceiver.ttl')
        doc = sbol3.Document()
        doc.read(sbol_path, sbol3.TURTLE)
        uri = 'https://synbiohub.org/public/igem/BBa_F2620/SubComponent3/Range1'
        range1 = doc.find(uri)
        self.assertIsNotNone(range1)
        self.assertEqual(1, range1.start)
        self.assertEqual(53, range1.end)

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
        ext = os.path.splitext(filename)[1]
        # drop the leading dot
        ext = ext[1:]
        ext_map = {
            'nt': sbol3.NTRIPLES,
            'ttl': sbol3.TURTLE,
            'rdf': sbol3.RDF_XML,
            'jsonld': sbol3.JSONLD,
            'jsonld_expanded': sbol3.JSONLD,
        }
        if ext in ext_map:
            return ext_map[ext]
        else:
            return None

    def test_read_all(self):
        # In lieu of round tripping the files, just make sure we can
        # read them all.
        #
        # This was an early test, before the library was complete and
        # the files could be round tripped.
        skip_list = self.skip_reading
        for f in self.find_all_files(SBOL3_LOCATION):
            basename = os.path.basename(f)
            if os.path.splitext(basename)[0] in skip_list:
                # print(f'Skipping {f}')
                continue
            rdf_type = self.rdf_type(f)
            if rdf_type is None:
                # Skip file types we don't know
                # print(f'Skipping {f} of type {rdf_type}')
                continue
            # print(f'Reading {f}')
            doc = sbol3.Document()
            doc.read(f, rdf_type)

    def run_round_trip_file(self, test_path, file_format):
        """Runs a round trip test on the file at the given path.
        Path can be relative or absolute.
        """
        filename = os.path.basename(test_path)
        test2_path = os.path.join(self.temp_out_dir, filename)
        # Read the document, then write it back to disk
        doc = sbol3.Document()
        doc.read(test_path, file_format)
        skip_list = self.skip_validation
        basename = os.path.basename(test_path)
        if os.path.splitext(basename)[0] not in skip_list:
            # Validate files that are not in the skip list
            report = doc.validate()
            if report:
                for item in report:
                    print(item)
                self.fail(f'got {len(report)} validation errors')

        doc.write(test2_path, file_format)

        # Read the newly written document and compare results
        doc2 = sbol3.Document()
        doc2.read(test2_path, file_format)
        # TODO: what about Document.compare()?
        # self.assertTrue(doc.compare(doc2))

        # Now compare the graphs in RDF
        g1 = rdflib.Graph()
        g1.parse(test_path, format=file_format)
        iso1 = rdflib.compare.to_isomorphic(g1)
        g2 = rdflib.Graph()
        g2.parse(test2_path, format=file_format)
        iso2 = rdflib.compare.to_isomorphic(g2)
        rdf_diff = rdflib.compare.graph_diff(iso1, iso2)
        if rdf_diff[1] or rdf_diff[2]:
            self.logger.warning('Detected %d different RDF triples in %s' %
                                (len(rdf_diff[1]) + len(rdf_diff[2]), test_path))
            if not self.logger.isEnabledFor(logging.DEBUG):
                self.logger.warning('Set environment variable %s to see details',
                                    DEBUG_ENV_VAR)
            for stmt in rdf_diff[1]:
                self.logger.debug('Only in original: %r', stmt)
            for stmt in rdf_diff[2]:
                self.logger.debug('Only in loaded: %r', stmt)
            self.fail('Differences in RDF detected')

    def test_sbol3_files(self):
        test_dir = SBOL3_LOCATION
        skip_list = self.skip_round_trip
        for test_file in self.find_all_files(test_dir):
            basename = os.path.basename(test_file)
            if os.path.splitext(basename)[0] in skip_list:
                self.logger.debug(f'Skipping {test_file}')
                continue
            file_format = self.rdf_type(test_file)
            if not file_format:
                continue
            with self.subTest(filename=test_file):
                self.setUp()
                self.run_round_trip_file(test_file, file_format)
                self.tearDown()

    def test_mixed_rdf(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/96
        test_file = os.path.join(TEST_RESOURCE_DIR, 'mixed-rdf.nt')
        self.run_round_trip_file(test_file, sbol3.NTRIPLES)

    def test_multi_type_sbol(self):
        # Load a file that includes an SBOL object that has multiple other
        # rdf:type properties
        test_file = os.path.join(TEST_RESOURCE_DIR, 'multi-type-sbol.nt')
        self.run_round_trip_file(test_file, sbol3.NTRIPLES)

    def test_multi_type_ext(self):
        # Load a file that includes an SBOL object that has multiple other
        # rdf:type properties
        test_file = os.path.join(TEST_RESOURCE_DIR, 'multi-type-ext.nt')
        self.run_round_trip_file(test_file, sbol3.NTRIPLES)

    def test_multi_type_ext_builder(self):
        class MultiTypeExtension(sbol3.TopLevel):
            def __init__(self, identity: str, type_uri: str):
                super().__init__(identity=identity, type_uri=type_uri)

        def mte_builder(identity: str = None,
                        type_uri: str = None) -> sbol3.Identified:
            return MultiTypeExtension(identity=identity, type_uri=type_uri)

        ext_type_uri = 'http://example.com/fake/Type1'
        test_file = os.path.join(TEST_RESOURCE_DIR, 'multi-type-ext.nt')
        try:
            sbol3.Document.register_builder(ext_type_uri, mte_builder)
            self.run_round_trip_file(test_file, sbol3.NTRIPLES)
        finally:
            # Reach behind the scenes to remove the registered builder
            del sbol3.Document._uri_type_map[ext_type_uri]


if __name__ == '__main__':
    unittest.main()
