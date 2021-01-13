import logging
import os
import tempfile
import unittest

import rdflib

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestDocument(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(level=logging.INFO)

    def test_read_ntriples(self):
        # Initial test of Document.read
        filename = 'model.nt'
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model',
                                 filename)
        doc = sbol3.Document()
        doc.read(test_path)
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file = os.path.join(tmpdirname, filename)
            doc.write(test_file, sbol3.NTRIPLES)

    def test_read_turtle(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model',
                                 'model.ttl')
        doc = sbol3.Document()
        doc.read(test_path, sbol3.TURTLE)

    def test_read_xml_model(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model',
                                 'model.rdf')
        doc = sbol3.Document()
        doc.read(test_path, sbol3.RDF_XML)
        self.assertIsNotNone(doc.find('https://sbolstandard.org/examples/toggle_switch'))
        self.assertIsNotNone(doc.find('toggle_switch'))
        self.assertIsNotNone(doc.find('https://sbolstandard.org/examples/model1'))
        # We have inferred the displayId of model1
        self.assertIsNotNone(doc.find('model1'))

    def test_read_turtle_interface(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'interface',
                                 'interface.ttl')
        doc = sbol3.Document()
        doc.read(test_path, sbol3.TURTLE)

    def test_read_turtle_toggle_switch(self):
        # Initial test of Document.read
        test_path = os.path.join(SBOL3_LOCATION, 'toggle_switch',
                                 'toggle_switch.ttl')
        doc = sbol3.Document()
        doc.read(test_path, sbol3.TURTLE)

    def test_add(self):
        doc = sbol3.Document()
        type_uri = 'https://github.com/synbiodex/sbol3#TestObj'
        obj1 = sbol3.SBOLObject('obj', type_uri)
        with self.assertRaises(TypeError):
            doc.add(obj1)
        seq = sbol3.Sequence('seq1')
        doc.add(seq)
        seq2 = doc.find(seq.identity)
        self.assertEqual(seq.identity, seq2.identity)

    def test_add_multiple(self):
        # Ensure that duplicate identities cannot be added to the document.
        # See https://github.com/SynBioDex/pySBOL3/issues/39
        document = sbol3.Document()
        namespace1 = sbol3.Namespace(identity=sbol3.SBOL3_NS)
        document.add(namespace1)
        namespace2 = sbol3.Namespace(identity=sbol3.SBOL3_NS)
        with self.assertRaises(ValueError):
            document.add(namespace2)

    def test_write(self):
        doc = sbol3.Document()
        doc.add(sbol3.Component('c1', sbol3.SBO_DNA))
        with tempfile.TemporaryDirectory() as tmpdirname:
            nt_file = os.path.join(tmpdirname, 'test_output.nt')
            doc.write(nt_file, sbol3.NTRIPLES)
            xml_file = os.path.join(tmpdirname, 'test_output.xml')
            doc.write(xml_file, sbol3.RDF_XML)
            # No format specified for these, doc.write now figures
            # that out on its own
            out_path = os.path.join(tmpdirname, 'test_output.rdf')
            doc.write(out_path)
            out_path = os.path.join(tmpdirname, 'test_output.ttl')
            doc.write(out_path)
            out_path = os.path.join(tmpdirname, 'test_output.jsonld')
            doc.write(out_path)

    def test_bind(self):
        doc = sbol3.Document()
        prefix = 'foo'
        ns1 = 'http://example.com/foo'
        doc.bind(prefix, ns1)
        self.assertEqual(ns1, doc._namespaces[prefix])

    def test_add_namespace(self):
        doc = sbol3.Document()
        prefix = 'foo'
        ns1 = 'http://example.com/foo'
        with self.assertWarns(DeprecationWarning):
            doc.addNamespace(ns1, prefix)

    def test_guess_format(self):
        doc = sbol3.Document()
        # Expect ValueError because '.foo' file extension is unknown
        with self.assertRaises(ValueError):
            doc.read('test.foo')
        # Expect ValueError because '.foo' file extension is unknown
        with self.assertRaises(ValueError):
            doc.write('test.foo')

    def test_empty_graph(self):
        # Ensure that an empty document generates an empty RDF graph
        doc = sbol3.Document()
        g = doc.graph()
        self.assertEqual(0, len(g))

    def test_graph(self):
        doc = sbol3.Document()
        doc.add(sbol3.Component('foo', sbol3.SBO_DNA))
        graph = doc.graph()
        self.assertEqual(3, len(graph))
        subjects = set()
        predicates = set()
        for s, p, _ in graph:
            subjects.add(s)
            predicates.add(p)
        # Expecting 1 subject, the component
        self.assertEqual(1, len(subjects))
        # Expecting 3 predicates
        self.assertEqual(3, len(predicates))
        self.assertIn(rdflib.RDF.type, predicates)
        # Convert predicates to strings for the remaining assertions
        predicates = [str(p) for p in predicates]
        self.assertIn(sbol3.SBOL_DISPLAY_ID, predicates)
        self.assertIn(sbol3.SBOL_TYPE, predicates)

    def test_write_string(self):
        # Make sure Document.write_string produces the same output
        # as Document.write. Must use sorted NTriples for this test
        # because other formats do not have a guaranteed order.
        filename = 'model.nt'
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model',
                                 filename)
        doc = sbol3.Document()
        doc.read(test_path)
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file = os.path.join(tmpdirname, filename)
            doc.write(test_file, sbol3.SORTED_NTRIPLES)
            with open(test_file, 'rb') as infile:
                expected = infile.read()
        actual = doc.write_string(sbol3.SORTED_NTRIPLES)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
