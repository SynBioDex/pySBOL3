import logging
import os
import tempfile
import unittest
from typing import Optional

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

    def make_namespace_checker(self, namespace: str):
        def namespace_checker(thing: sbol3.Identified):
            # TopLevel has namespace, Identified does not
            if hasattr(thing, 'namespace'):
                self.assertEqual(namespace, thing.namespace)
            self.assertTrue(thing.identity.startswith(namespace))
        return namespace_checker

    def make_document_checker(self, document: Optional[sbol3.Document]):
        def document_checker(thing: sbol3.Identified):
            self.assertEqual(document, thing.document)
        return document_checker

    def test_file_extension(self):
        """ Test obtaining standard extensions from file format"""
        file_format_1 = sbol3.SORTED_NTRIPLES
        file_format_2 = sbol3.RDF_XML
        file_format_3 = 'Test_Format'
        # 1. testing for sorted ntriples
        extension_1 = sbol3.Document.file_extension(file_format_1)
        self.assertEqual(extension_1, '.nt')
        # 2. testing for rdf xml
        extension_2 = sbol3.Document.file_extension(file_format_2)
        self.assertEqual(extension_2, '.xml')
        # 3. for invalid file formats, valueError must be raised
        with self.assertRaises(ValueError):
            extension_3 = sbol3.Document.file_extension(file_format_3)

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
        added_seq = doc.add(seq)
        # Document.add should return the object
        # See https://github.com/SynBioDex/pySBOL3/issues/272
        self.assertEqual(seq, added_seq)
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

    def test_add_iterable(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/311
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        objects = [sbol3.Component(name, types=[sbol3.SBO_DNA])
                   for name in ['foo', 'bar', 'baz' 'quux']]
        result = doc.add(objects)
        self.assertEqual(len(objects), len(result))
        self.assertListEqual(objects, result)
        #
        # Test adding a non-TopLevel in a list
        doc = sbol3.Document()
        objects = [sbol3.Component(name, types=[sbol3.SBO_DNA])
                   for name in ['foo', 'bar', 'baz' 'quux']]
        objects.insert(2, 'non-TopLevel')
        with self.assertRaises(TypeError):
            doc.add(objects)

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

    def test_json_ld_parser_bug(self):
        # See https://github.com/RDFLib/rdflib/issues/1443
        # See https://github.com/SynBioDex/pySBOL3/issues/329
        # The rdflib json-ld parser adds a trailing slash onto URLs that
        # have no path. Add this test to notice when the bug eventually
        # gets fixed.
        test_dir = os.path.join(SBOL3_LOCATION, 'entity', 'model')
        json_ld_path = os.path.join(test_dir, 'model.jsonld')
        turtle_path = os.path.join(test_dir, 'model.ttl')
        doc_json_ld = sbol3.Document()
        doc_json_ld.read(json_ld_path)
        doc_turtle = sbol3.Document()
        doc_turtle.read(turtle_path)
        # Find the target object in the documents
        model_uri = 'https://sbolstandard.org/examples/model1'
        m_json_ld = doc_json_ld.find(model_uri)
        self.assertIsNotNone(m_json_ld)
        m_turtle = doc_turtle.find(model_uri)
        self.assertIsNotNone(m_turtle)
        self.assertEqual(m_turtle.source, m_json_ld.source)
        self.assertEqual(m_turtle.namespace, m_json_ld.namespace)

    def test_read_with_default_namespace(self):
        # Test reading a file when the default namespace is set
        # See https://github.com/SynBioDex/pySBOL3/issues/337
        sbol3.set_namespace('http://example.com')
        test_path = os.path.join(SBOL3_LOCATION, 'toggle_switch',
                                 'toggle_switch.ttl')
        doc = sbol3.Document()
        doc.read(test_path)

    def test_read_default_namespace(self):
        # This is a modified version of the initial bug report for
        # https://github.com/SynBioDex/pySBOL3/issues/337
        doc = sbol3.Document()
        sbol3.set_namespace('http://foo.org')
        doc.add(sbol3.Sequence('bar'))
        self.assertEqual(0, len(doc.validate()))
        file_format = sbol3.SORTED_NTRIPLES
        data = doc.write_string(file_format=file_format)

        doc2 = sbol3.Document()
        doc2.read_string(data, file_format=file_format)  # Successful read

        sbol3.set_namespace('http://baz.com/')
        doc3 = sbol3.Document()
        doc3.read_string(data, file_format=file_format)

    def test_jsonld_no_vocab(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/349
        doc = sbol3.Document()
        doc_string = doc.write_string(file_format=sbol3.JSONLD)
        self.assertNotIn('@vocab', doc_string)

    def test_remove_from_document(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        c1 = sbol3.Component('c1', types=[sbol3.SBO_DNA])
        doc.add(c1)
        self.assertIn(c1, doc)
        self.assertEqual(doc, c1.document)
        doc.remove_object(c1)
        # Now c1 should not be in the document, but c1 should still
        # have the document pointer. Document.remove_object does not
        # update the object's document pointer.
        self.assertNotIn(c1, doc)
        self.assertEqual(doc, c1.document)

    def test_remove_from_document_identified(self):
        # Test removing a non-TopLevel from the document. This should
        # not give an error
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        # This should quietly succeed because the string is not in the
        # document
        doc.remove_object('foo')
        lsc = sbol3.LocalSubComponent(types=[sbol3.SBO_DNA])
        # This should also quietly succeed because the local subcomponent
        # is also not in the document
        doc.remove_object(lsc)

    def test_remove(self):
        # Test removing some objects, and verify that the document
        # pointers are gone
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        obj1_uri = 'https://sbolstandard.org/examples/MulticellularSystem'
        obj2_uri = 'https://sbolstandard.org/examples/SenderSystem'
        obj1 = doc.find(obj1_uri)
        self.assertIsInstance(obj1, sbol3.TopLevel)
        self.assertIsNotNone(obj1)
        self.assertIn(obj1, doc)
        self.assertEqual(doc, obj1.document)
        for feature in obj1.features:
            self.assertEqual(doc, feature.document)
        for constraint in obj1.constraints:
            self.assertEqual(doc, constraint.document)
        obj2 = doc.find(obj2_uri)
        self.assertIsInstance(obj2, sbol3.TopLevel)
        self.assertIsNotNone(obj2)
        self.assertIn(obj2, doc)
        doc.remove([obj1, obj2])
        self.assertNotIn(obj1, doc)
        self.assertIsNone(obj1.document)
        # Verify that obj1's children have no document pointer
        for feature in obj1.features:
            self.assertIsNone(feature.document)
        for constraint in obj1.constraints:
            self.assertIsNone(constraint.document)
        self.assertNotIn(obj2, doc)
        self.assertIsNone(obj2.document)
        # Verify that obj2's children have no document pointer
        for feature in obj2.features:
            self.assertIsNone(feature.document)
        for constraint in obj2.constraints:
            self.assertIsNone(constraint.document)

    def test_iterable(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        # Make sure the document is iterable
        self.assertIsNotNone(iter(doc))
        all_objs = list(doc)
        # Make sure the objects returned by the iterator match the top
        # level objects in the document
        self.assertListEqual(doc.objects, all_objs)

    def test_migrate(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        orig_len = len(doc)
        doc2 = sbol3.Document()
        doc2.migrate(doc)
        self.assertEqual(orig_len, len(doc2))
        self.assertEqual(0, len(doc))

    def test_change_object_namespace(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        obj = doc.objects[0]
        old_identity = obj.identity
        doc.change_object_namespace([obj], namespace)
        self.assertEqual(namespace, obj.namespace)
        self.assertNotEqual(old_identity, obj.identity)
        self.assertTrue(obj.identity.startswith(namespace))

    def test_change_object_namespace_ref(self):
        # test with a referenced object, like a component with a sequence
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        doc = sbol3.Document()
        s1 = sbol3.Sequence('s1')
        c1 = sbol3.Component('c1', types=[sbol3.SBO_DNA], sequences=[s1])
        doc.add([s1, c1])
        self.assertEqual(2, len(doc))
        self.assertEqual(s1.identity, c1.sequences[0])
        ns2 = 'https://example.com/test_ns'
        s1_identity = s1.identity
        c1_identity = c1.identity
        doc.change_object_namespace([s1, c1], ns2)
        self.assertEqual(ns2, s1.namespace)
        self.assertEqual(ns2, c1.namespace)
        self.assertTrue(s1.identity.startswith(ns2))
        self.assertTrue(c1.identity.startswith(ns2))
        self.assertNotEqual(s1_identity, s1.identity)
        self.assertNotEqual(c1_identity, c1.identity)
        self.assertEqual(s1.identity, c1.sequences[0])

    def test_change_object_namespace_doc(self):
        # test with a full document of objects, changing the entire document
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        doc.change_object_namespace(doc.objects, namespace)

        # Make sure every object has the new namespace
        namespace_checker = self.make_namespace_checker(namespace)
        for obj in doc.objects:
            obj.traverse(namespace_checker)

    def test_change_object_namespace_errors(self):
        # Test bad arguments, like non-top-levels
        namespace = 'https://github.com/synbiodex/pysbol3'
        new_namespace = 'https://example.com/test_ns'
        sbol3.set_namespace(namespace)
        doc = sbol3.Document()
        # Non-TopLevel should raise ValueError
        i1 = sbol3.Interaction([sbol3.SBO_INHIBITION])
        with self.assertRaises(ValueError):
            doc.change_object_namespace([i1], new_namespace)

    def test_clone(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        # Clone the document
        clones = doc.clone()
        # We should have the same number of objects in the clone list
        self.assertEqual(len(doc), len(clones))
        # Now spot check the features of an object
        target_identity = 'https://sbolstandard.org/examples/MulticellularSystem'
        orig = doc.find(target_identity)
        clone = None
        for c in clones:
            if c.identity == target_identity:
                clone = c
                break
        # Be sure we found the target clone
        self.assertIsNotNone(clone)
        orig_feature_identities = [f.identity for f in orig.features]
        clone_feature_identities = [f.identity for f in clone.features]
        self.assertEqual(orig_feature_identities, clone_feature_identities)
        # There are probably more tests we can do...

    def test_copy(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.ttl')
        doc = sbol3.Document()
        doc.read(test_path)
        copies1 = sbol3.copy(doc)
        self.assertEqual(len(doc), len(copies1))
        document_checker = self.make_document_checker(None)
        for obj in copies1:
            obj.traverse(document_checker)
        # Verify that the copies get the new namespace
        copies2 = sbol3.copy(doc, into_namespace=namespace)
        document_checker = self.make_document_checker(None)
        namespace_checker = self.make_namespace_checker(namespace)
        for obj in copies2:
            obj.traverse(document_checker)
            obj.traverse(namespace_checker)
        # Verify new namespace AND new document
        namespace3 = 'https://github.com/synbiodex/pysbol3/copytest'
        doc3 = sbol3.Document()
        copies3 = sbol3.copy(doc, into_namespace=namespace3, into_document=doc3)
        document_checker = self.make_document_checker(doc3)
        namespace_checker = self.make_namespace_checker(namespace3)
        for obj in copies3:
            obj.traverse(document_checker)
            obj.traverse(namespace_checker)

    def test_copy_stability(self):
        # Test the stability of naming of objects across copies.
        # See https://github.com/SynBioDex/pySBOL3/issues/231
        #
        # Strategy: create an object with 10+ children of the same
        # type. Add to a document and serialize the document. Load the
        # serialized document. Copy the object to a new document.
        # Serialize the new document. Compare the serializations. If we
        # use sorted ntriples, the serializations should be the same.
        # This will demonstrate that we maintain names properly despite
        # the inherently unordered nature of SBOL.
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', types=[sbol3.SBO_DNA])
        # Create a double-digit number of children to test sort of 10, 11, 1, etc.
        for i in range(12):
            instance_of_uri = f'https://example.com/instance/i{i}'
            c1.features.append(sbol3.SubComponent(instance_of=instance_of_uri))
        doc1 = sbol3.Document()
        doc1.add(c1)
        # Serialize to string
        doc1_string = doc1.write_string(sbol3.SORTED_NTRIPLES)
        self.assertIsNotNone(doc1_string)
        # Load the serialized document into a new document
        tmp_doc = sbol3.Document()
        tmp_doc.read_string(doc1_string, sbol3.SORTED_NTRIPLES)
        # Locate the top level to copy
        tmp_c1 = tmp_doc.find('c1')
        self.assertIsNotNone(tmp_c1)
        self.assertIsInstance(tmp_c1, sbol3.TopLevel)
        # Copy the top level into a new document
        doc2 = sbol3.Document()
        sbol3.copy([tmp_c1], into_document=doc2)
        doc2_string = doc2.write_string(sbol3.SORTED_NTRIPLES)
        # Verify that the serializations are identical
        self.assertEqual(doc1_string, doc2_string)


if __name__ == '__main__':
    unittest.main()
