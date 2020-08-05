import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestDocument(unittest.TestCase):

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
        # model1 does not have a display id at the moment,
        # so it cannot be found by its display id.
        self.assertIsNone(doc.find('model1'))

    def test_read_xml_interface(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'interface', 'interface.rdfxml.sbol')
        doc = sbol3.Document()
        doc.read(test_path, format='xml')
