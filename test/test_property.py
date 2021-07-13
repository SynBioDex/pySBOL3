import math
import posixpath
import unittest
from collections.abc import Iterable

import rdflib

import sbol3


class TestProperty(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_slice_assignment(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        self.assertEqual([], c.roles)
        c.roles.append(sbol3.SO_PROMOTER)
        self.assertEqual([sbol3.SO_PROMOTER], c.roles)
        expected = [rdflib.URIRef(item) for item in c.roles]
        self.assertEqual(expected, c._properties[sbol3.SBOL_ROLE])

        c.roles.append(sbol3.SO_CDS)
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_CDS], c.roles)
        expected = [rdflib.URIRef(item) for item in c.roles]
        self.assertEqual(expected, c._properties[sbol3.SBOL_ROLE])

        c.roles[1] = sbol3.CHEBI_EFFECTOR
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.CHEBI_EFFECTOR], c.roles)
        # Make sure the underlying representation is correct
        expected = [rdflib.URIRef(item) for item in c.roles]
        self.assertEqual(expected, c._properties[sbol3.SBOL_ROLE])

        c.roles.append(sbol3.SO_RBS)
        expected = [sbol3.SO_PROMOTER, sbol3.CHEBI_EFFECTOR, sbol3.SO_RBS]
        self.assertEqual(expected, c.roles)
        expected = [rdflib.URIRef(item) for item in c.roles]
        self.assertEqual(expected, c._properties[sbol3.SBOL_ROLE])

        # Replace the first two elements by slice replacement
        c.roles[0:2] = [sbol3.SO_OPERATOR, sbol3.SO_MRNA]
        expected = [sbol3.SO_OPERATOR, sbol3.SO_MRNA, sbol3.SO_RBS]
        self.assertEqual(expected, c.roles)
        expected = [rdflib.URIRef(item) for item in c.roles]
        self.assertEqual(expected, c._properties[sbol3.SBOL_ROLE])

    def test_boolean_property(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        c.boolean_attribute = sbol3.BooleanProperty(c, 'http://example.org#foo',
                                                    0, 1, [])
        c.boolean_attribute = True
        self.assertEqual(type(c.boolean_attribute), bool)

    def test_bounds(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        c.boolean_attribute = sbol3.BooleanProperty(c, 'http://example.org#foo',
                                                    0, math.inf, [])
        self.assertTrue(hasattr(c.boolean_attribute, '__iter__'))
        with self.assertRaises(TypeError):
            c.boolean_attribute = True
        c.int_attribute = sbol3.IntProperty(c, 'http://example.org#foo',
                                            0, math.inf, [])
        self.assertTrue(hasattr(c.int_attribute, '__iter__'))
        with self.assertRaises(TypeError):
            c.int_attribute = 0

    def test_iadd(self):
        # This is a test for the += operator, which is implemented as __iadd__()
        # When += is invoked the default __iadd__() implementation calls insert()
        # and calls set(). That confuses our auto-numbering of child object
        # identities.
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        doc.add(c1)
        lsc1 = sbol3.LocalSubComponent([sbol3.SBO_DNA])
        c1.features += [lsc1]
        self.assertEqual('LocalSubComponent1', lsc1.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc1.display_id),
                         lsc1.identity)
        # TODO: Add checks for document at each step below
        self.assertEqual(doc, lsc1.document)

        lsc2 = sbol3.LocalSubComponent([sbol3.SBO_DNA])
        c1.features += [lsc2]
        # Make sure lsc1 did not get renamed
        self.assertEqual('LocalSubComponent1', lsc1.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc1.display_id),
                         lsc1.identity)
        self.assertEqual(doc, lsc1.document)
        self.assertEqual('LocalSubComponent2', lsc2.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc2.display_id),
                         lsc2.identity)
        self.assertEqual(doc, lsc2.document)

        lsc3 = sbol3.LocalSubComponent([sbol3.SBO_DNA])
        lsc4 = sbol3.LocalSubComponent([sbol3.SBO_DNA])
        c1.features += [lsc3, lsc4]
        # Make sure lsc1 did not get renamed
        self.assertEqual('LocalSubComponent1', lsc1.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc1.display_id),
                         lsc1.identity)
        self.assertEqual(doc, lsc1.document)
        # Make sure lsc2 did not get renamed
        self.assertEqual('LocalSubComponent2', lsc2.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc2.display_id),
                         lsc2.identity)
        self.assertEqual(doc, lsc2.document)
        self.assertEqual('LocalSubComponent3', lsc3.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc3.display_id),
                         lsc3.identity)
        self.assertEqual(doc, lsc3.document)
        self.assertEqual('LocalSubComponent4', lsc4.display_id)
        self.assertEqual(posixpath.join(c1.identity, lsc4.display_id),
                         lsc4.identity)
        self.assertEqual(doc, lsc4.document)

    def test_not_iterable(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        self.assertIsInstance(c1.types, Iterable)
        with self.assertRaises(TypeError):
            c1.types = sbol3.SBO_PROTEIN
        with self.assertRaises(TypeError):
            c1.types = object()

    def test_attribute_name(self):
        # Verify that a property can figure out what its attribute name is.
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        types_property = c1.__dict__['types']
        aname = types_property.attribute_name
        self.assertEqual('types', aname)
        features_property = c1.__dict__['features']
        aname = features_property.attribute_name
        self.assertEqual('features', aname)


if __name__ == '__main__':
    unittest.main()
