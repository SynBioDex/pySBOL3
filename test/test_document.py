import logging
import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestDocument(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(level=logging.INFO)

    def test_read_ntriples(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.ntriples.sbol')
        doc = sbol3.Document()
        doc.read(test_path, format='n3')

    def test_read_turtle(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.turtle.sbol')
        doc = sbol3.Document()
        doc.read(test_path, format='turtle')

    def test_read_xml_model(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.rdfxml.sbol')
        doc = sbol3.Document()
        doc.read(test_path, format='xml')
        self.assertIsNotNone(doc.find('https://sbolstandard.org/examples/toggle_switch'))
        self.assertIsNotNone(doc.find('toggle_switch'))
        self.assertIsNotNone(doc.find('https://sbolstandard.org/examples/model1'))
        # We have inferred the displayId of model1
        self.assertIsNotNone(doc.find('model1'))

    def test_read_xml_interface(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'interface', 'interface.rdfxml.sbol')
        doc = sbol3.Document()
        doc.read(test_path, format='xml')

    def test_read_turtle_toggle_switch(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'toggle_switch', 'toggle_switch.turtle.sbol')
        doc = sbol3.Document()
        doc.read(test_path, format='turtle')

    def test_add(self):
        doc = sbol3.Document()
        obj1 = sbol3.SBOLObject()
        with self.assertRaises(TypeError):
            doc.add(obj1)
        seq_uri = 'https://github.com/synbiodex/pysbol3/seq1'
        seq = sbol3.Sequence()
        seq.identity = seq_uri
        doc.add(seq)
        seq2 = doc.find(seq_uri)
        self.assertEqual(seq.identity, seq2.identity)


if __name__ == '__main__':
    unittest.main()
