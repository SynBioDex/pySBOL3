import logging
import os
import tempfile
import unittest

import rdflib

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')
TEST_RESOURCE_DIR = os.path.join(MODULE_LOCATION, 'resources')


class TestDocument(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(level=logging.INFO)

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

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
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        non_top_level = sbol3.Interface()
        with self.assertRaises(TypeError):
            doc.add(non_top_level)
        seq = sbol3.Sequence('seq1')
        doc.add(seq)
        seq2 = doc.find(seq.identity)
        self.assertEqual(seq.identity, seq2.identity)

    def test_add_multiple(self):
        # Ensure that duplicate identities cannot be added to the document.
        # See https://github.com/SynBioDex/pySBOL3/issues/39
        document = sbol3.Document()
        experiment1 = sbol3.Experiment(identity=sbol3.SBOL3_NS)
        document.add(experiment1)
        experiment2 = sbol3.Experiment(identity=sbol3.SBOL3_NS)
        with self.assertRaises(ValueError):
            document.add(experiment2)

    def test_write(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
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
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        doc.add(sbol3.Component('foo', sbol3.SBO_DNA))
        graph = doc.graph()
        self.assertEqual(4, len(graph))
        subjects = set()
        predicates = set()
        for s, p, _ in graph:
            subjects.add(s)
            predicates.add(p)
        # Expecting 1 subject, the component
        self.assertEqual(1, len(subjects))
        # Expecting 3 predicates
        self.assertEqual(4, len(predicates))
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
            with open(test_file, 'r') as infile:
                expected = infile.read()
        actual = doc.write_string(sbol3.SORTED_NTRIPLES)
        self.assertEqual(expected, actual)

    def test_validate(self):
        # Test the document level validation
        # This should validate all the objects in the document
        # and return a report containing all errors and warnings.
        doc = sbol3.Document()
        c1 = sbol3.Component('https://github.com/synbiodex/pysbol3/c1',
                             sbol3.SBO_DNA)
        doc.add(c1)
        s1 = sbol3.Sequence('https://github.com/synbiodex/pysbol3/s1')
        doc.add(s1)
        start = 10
        end = 1
        r = sbol3.Range(s1, start, end)
        sf = sbol3.SequenceFeature([r])
        c1.features.append(sf)
        report = doc.validate()
        # We should find the validation issue in the Range
        self.assertEqual(1, len(report))

    def test_validate_invalid_doc(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/257
        # This should return an error from the shacl validation
        doc = sbol3.Document()
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.nt')
        doc.read(test_path)
        report = doc.validate()
        # Confirm that the original document is valid
        self.assertEqual(0, len(report))
        # Now modify an object to be invalid
        uri = 'https://sbolstandard.org/examples/rbs_luxR'
        c = doc.find(uri)
        self.assertIsNotNone(c)
        c._properties[sbol3.SBOL_TYPE] = []
        report = doc.validate()
        # Confirm that the modified document is not valid
        #
        # The lack of a component.type is a violation that should be
        # detected by the shacl validation. This currently causes 2
        # validation errors, one for too few values for the type property,
        # and the other for less than 1 value on the type property.
        self.assertEqual(2, len(report))

    def test_find_all(self):
        test_files = {
            os.path.join(SBOL3_LOCATION, 'entity', 'model',
                         'model.nt'): 2,
            os.path.join(SBOL3_LOCATION, 'multicellular',
                         'multicellular.nt'): 75,
        }
        for file, count in test_files.items():
            doc = sbol3.Document()
            doc.read(file)
            found = doc.find_all(lambda _: True)
            self.assertEqual(count, len(found))

    def test_find_all2(self):
        file = os.path.join(SBOL3_LOCATION, 'multicellular',
                            'multicellular.nt')
        doc = sbol3.Document()
        doc.read(file)
        # Find all instances of Participation
        found = doc.find_all(lambda obj: isinstance(obj, sbol3.Participation))
        self.assertEqual(11, len(found))

    def test_traverse_all(self):
        traversed_list = []

        def my_traverser(obj: sbol3.Identified):
            traversed_list.append(obj)
        file = os.path.join(SBOL3_LOCATION, 'multicellular',
                            'multicellular.nt')
        doc = sbol3.Document()
        doc.read(file)
        doc.traverse(my_traverser)
        self.assertEqual(75, len(traversed_list))

    def test_traverse_participations(self):
        # Traverse all and only the participations
        traversed_list = []

        def my_traverser(obj: sbol3.Identified):
            if isinstance(obj, sbol3.Participation):
                traversed_list.append(obj)
        file = os.path.join(SBOL3_LOCATION, 'multicellular',
                            'multicellular.nt')
        doc = sbol3.Document()
        doc.read(file)
        doc.traverse(my_traverser)
        self.assertEqual(11, len(traversed_list))

    def test_builder_lookup(self):
        # Test looking up a builder function
        # See https://github.com/SynBioDex/pySBOL3/issues/175
        doc = sbol3.Document()
        builder = doc.builder(sbol3.SBOL_EXTERNALLY_DEFINED)
        self.assertIsNotNone(builder)
        self.assertTrue(callable(builder))
        with self.assertRaises(ValueError):
            doc.builder('http://example.com/SomeType')
        with self.assertRaises(ValueError):
            doc.builder(None)

    def test_other_rdf_round_trip(self):
        filename = 'mixed-rdf.nt'
        test_file = os.path.join(MODULE_LOCATION, 'resources', filename)
        doc = sbol3.Document()
        doc.read(test_file)
        c_uri = 'http://example.com/sbol3/c1'
        c = doc.find(c_uri)
        self.assertIsNotNone(c)
        self.assertEqual([sbol3.SBO_DNA], c.types)
        c.types = [sbol3.SBO_PROTEIN]
        self.assertEqual([sbol3.SBO_PROTEIN], c.types)
        # Now round trip the file and make sure the
        # types property remains the same
        doc2 = sbol3.Document()
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_file = os.path.join(tmpdirname, filename)
            doc.write(tmp_file)
            doc2.read(tmp_file)
        c2 = doc2.find(c_uri)
        self.assertIsNotNone(c2)
        self.assertEqual([sbol3.SBO_PROTEIN], c2.types)

    def test_multi_type_sbol(self):
        # Load a file that includes an SBOL object that has multiple other
        # rdf:type properties
        test_file = os.path.join(TEST_RESOURCE_DIR, 'multi-type-sbol.nt')
        doc = sbol3.Document()
        doc.read(test_file)
        c_uri = 'http://example.com/sbol3/c1'
        c = doc.find(c_uri)
        self.assertIsNotNone(c)
        self.assertEqual(3, len(c._rdf_types))
        self.assertEqual(sbol3.SBOL_COMPONENT, c.type_uri)
        self.assertIsInstance(c, sbol3.Component)

    def test_multi_type_ext(self):
        # Load a file that includes an SBOL object that has multiple other
        # rdf:type properties
        test_file = os.path.join(TEST_RESOURCE_DIR, 'multi-type-ext.nt')
        doc = sbol3.Document()
        doc.read(test_file)
        uri = 'http://example.com/sbol3/c1'
        x = doc.find(uri)
        self.assertIsNotNone(x)
        self.assertEqual(3, len(x._rdf_types))
        self.assertNotEqual(sbol3.SBOL_TOP_LEVEL, x.type_uri)
        self.assertIsInstance(x, sbol3.CustomTopLevel)

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
            doc = sbol3.Document()
            doc.read(test_file)
            uri = 'http://example.com/sbol3/c1'
            x = doc.find(uri)
            self.assertIsNotNone(x)
            self.assertEqual(3, len(x._rdf_types))
            self.assertEqual(ext_type_uri, x.type_uri)
            self.assertIsInstance(x, MultiTypeExtension)
        finally:
            # Reach behind the scenes to remove the registered builder
            del sbol3.Document._uri_type_map[ext_type_uri]

    def test_variable_feature_shacl(self):
        # See https://github.com/SynBioDex/sbol-shacl/issues/4
        # This file should be valid. Ensure we are handling
        # VariableFeature in the SHACL rules
        test_file = os.path.join(TEST_RESOURCE_DIR, 'simple_library.nt')
        doc = sbol3.Document()
        doc.read(test_file)
        report = doc.validate()
        self.assertEqual(0, len(report))


if __name__ == '__main__':
    unittest.main()
