import math
import os
import tempfile
import unittest

import rdflib

import sbol3


PYSBOL3_CUSTOM_TOP = 'https://github.com/synbiodex/pysbol3#customTop'
PYSBOL3_CUSTOM_BOOL = 'https://github.com/synbiodex/pysbol3#customBool'
PYSBOL3_CUSTOM_CHILD = 'https://github.com/synbiodex/pysbol3#customChildren'
PYSBOL3_CUSTOM_IDENTIFIED = 'https://github.com/synbiodex/pysbol3#customIdentified'
PYSBOL3_CUSTOM_INT = 'https://github.com/synbiodex/pysbol3#customInt'


class CustomTopClass(sbol3.CustomTopLevel):
    def __init__(self, identity, type_uri=PYSBOL3_CUSTOM_TOP):
        super().__init__(identity, type_uri)
        # Also test the boolean list while we're here
        self.foo_bool = sbol3.BooleanProperty(self, PYSBOL3_CUSTOM_BOOL,
                                              0, math.inf)
        self.children = sbol3.OwnedObject(self, PYSBOL3_CUSTOM_CHILD, 0, math.inf)


class CustomIdentifiedClass(sbol3.CustomIdentified):
    def __init__(self, type_uri=PYSBOL3_CUSTOM_IDENTIFIED, identity=None):
        super().__init__(type_uri, identity=identity)
        # Also test the int list while we're here
        self.foo_int = sbol3.IntProperty(self, PYSBOL3_CUSTOM_INT,
                                         0, math.inf)


class TestCustomTopLevel(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        sbol3.Document.register_builder(PYSBOL3_CUSTOM_TOP, CustomTopClass)

    @classmethod
    def tearDownClass(cls) -> None:
        # Go behind the scenes to clean up
        # TODO: should there be a way to deregister a builder?
        store = sbol3.Document._uri_type_map
        if PYSBOL3_CUSTOM_TOP in store:
            del store[PYSBOL3_CUSTOM_TOP]

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        custom_type = 'https://github.com/synbiodex/pysbol3/CustomType'
        ctl = sbol3.CustomTopLevel('custom1', custom_type)
        self.assertEqual(custom_type, ctl.type_uri)
        # Go behind the scenes to verify
        expected = [custom_type, sbol3.SBOL_TOP_LEVEL]
        self.assertCountEqual(expected, ctl._rdf_types)

    # TODO: We really want to verify the serialization of the custom top
    #       level as well. There is no Document.writeString() yet.

    def test_round_trip(self):
        # Test the boolean list property, which is not used by the
        # core SBOL 3 data model
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        obj_name = 'bool_test'
        obj = CustomTopClass(obj_name)
        self.assertEqual([], obj.foo_bool)
        obj.foo_bool.append(True)
        obj.foo_bool.append(False)
        self.assertEqual([True, False], obj.foo_bool)
        doc = sbol3.Document()
        doc.add(obj)
        doc2 = sbol3.Document()
        # Round trip the document
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file = os.path.join(tmpdirname, 'custom.nt')
            doc.write(test_file, sbol3.NTRIPLES)
            doc2.read(test_file, sbol3.NTRIPLES)
        obj2 = doc2.find(obj_name)
        # The lists are necessarily unordered because of RDF
        # Compare specially
        self.assertCountEqual([True, False], obj2.foo_bool)

    def test_none_identity(self):
        # Make sure a ValueError is raised if None is passed
        # as a CustomTopLevel identity. And also if identity
        # is an empty string or not a string.
        with self.assertRaises(ValueError):
            obj = CustomTopClass(None)
        with self.assertRaises(ValueError):
            obj = CustomTopClass('')
        with self.assertRaises(ValueError):
            obj = CustomTopClass(3)


class TestCustomIdentified(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        sbol3.Document.register_builder(PYSBOL3_CUSTOM_TOP, CustomTopClass)
        sbol3.Document.register_builder(PYSBOL3_CUSTOM_IDENTIFIED, CustomIdentifiedClass)

    @classmethod
    def tearDownClass(cls) -> None:
        # Go behind the scenes to clean up
        # TODO: should there be a way to deregister a builder?
        store = sbol3.Document._uri_type_map
        for uri in [PYSBOL3_CUSTOM_TOP, PYSBOL3_CUSTOM_IDENTIFIED]:
            if uri in store:
                del store[uri]

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        custom_type = 'https://github.com/synbiodex/pysbol3/CustomType'
        ctl = sbol3.CustomIdentified(identity='custom1',
                                     type_uri=custom_type)
        self.assertEqual(custom_type, ctl.type_uri)
        # Go behind the scenes to verify
        expected = [custom_type, sbol3.SBOL_IDENTIFIED]
        self.assertCountEqual(expected, ctl._rdf_types)

    # TODO: We really want to verify the serialization of the custom
    #       identified as well. We need to attach it to a top level
    #       to see that work.

    def test_round_trip(self):
        # Test the int list property, which is not used by the
        # core SBOL 3 data model
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        obj = CustomIdentifiedClass()
        self.assertEqual([], obj.foo_int)
        obj.foo_int.append(7)
        obj.foo_int.append(14)
        self.assertEqual([7, 14], obj.foo_int)

        tl_name = 'my_obj'
        tl = CustomTopClass(tl_name)
        tl.children.append(obj)
        doc = sbol3.Document()
        doc.add(tl)
        doc2 = sbol3.Document()
        # Round trip the document
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file = os.path.join(tmpdirname, 'custom.nt')
            doc.write(test_file, sbol3.NTRIPLES)
            doc2.read(test_file, sbol3.NTRIPLES)
        tl2 = doc2.find(tl_name)
        obj2 = tl2.children[0]
        # The lists are necessarily unordered because of RDF
        # Compare specially
        self.assertCountEqual([7, 14], obj2.foo_int)


if __name__ == '__main__':
    unittest.main()
