import logging
import os
import subprocess
import sys
import unittest
import tempfile
import shutil
import rdflib
import rdflib.compare

import sbol3

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_DIR = os.path.join(os.path.dirname(TEST_DIR), 'examples')
CIRCUIT_EXAMPLE = os.path.join(EXAMPLE_DIR, 'circuit.py')
EXPECTED_CIRCUIT = os.path.join(TEST_DIR, 'resources', 'circuit.nt')


class TestExamples(unittest.TestCase):

    def setUp(self):
        sbol3.set_defaults()
        # Create temp directory
        self.temp_out_dir = tempfile.mkdtemp()
        self.logger = logging.getLogger('sbol3.test')
        if not self.logger.hasHandlers():
            logging.basicConfig()

    def tearDown(self):
        # Remove directory after the test
        if self.temp_out_dir:
            shutil.rmtree(self.temp_out_dir)
            self.temp_out_dir = None
        sbol3.set_defaults()

    def test_circuit_example(self):
        cmd = [sys.executable, CIRCUIT_EXAMPLE]
        subprocess.check_call(cmd, cwd=self.temp_out_dir)
        out_path = os.path.join(self.temp_out_dir, 'circuit.nt')
        self.assertTrue(os.path.exists(out_path))
        # Load the output
        actual_graph = rdflib.Graph()
        actual_graph.parse(out_path, format=sbol3.NTRIPLES)
        actual_iso = rdflib.compare.to_isomorphic(actual_graph)
        # Load the expected output
        expected_graph = rdflib.Graph()
        expected_graph.parse(EXPECTED_CIRCUIT, format=sbol3.NTRIPLES)
        expected_iso = rdflib.compare.to_isomorphic(expected_graph)
        rdf_diff = rdflib.compare.graph_diff(expected_iso, actual_iso)
        if rdf_diff[1] or rdf_diff[2]:
            self.logger.warning('Detected %d different RDF triples in %s' %
                                (len(rdf_diff[1]) + len(rdf_diff[2]), out_path))
            for stmt in rdf_diff[1]:
                self.logger.warning('Only in expected: %r', stmt)
            for stmt in rdf_diff[2]:
                self.logger.warning('Only in actual: %r', stmt)
            self.fail('Differences in RDF detected')


if __name__ == '__main__':
    unittest.main()
