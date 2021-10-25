import posixpath
import unittest
import uuid

import rdflib

import sbol3


class TestCollection(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        collection = sbol3.Collection('collection1')
        self.assertIsNotNone(collection)
        self.assertEqual(0, len(collection.members))
        self.assertEqual(sbol3.SBOL_COLLECTION, collection.type_uri)

    def test_read(self):
        identity = 'https://github.com/synbiodex/pysbol3/collection1'
        nt_data = f'<{identity}> <{rdflib.RDF.type}> <{sbol3.SBOL_COLLECTION}> .'
        doc = sbol3.Document()
        doc.read_string(nt_data, 'ttl')
        collection = doc.find(identity)
        self.assertIsNotNone(collection)
        self.assertIsInstance(collection, sbol3.Collection)

    def test_member_property(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        self.assertTrue(hasattr(sbol3, 'SBOL_MEMBER'))
        collection = sbol3.Collection('collection1')
        self.assertIn(sbol3.SBOL_MEMBER, collection._properties)
        self.assertNotIn(sbol3.SBOL_ORIENTATION, collection._properties)
        uris = ['https://github.com/synbiodex/pysbol3/thing1',
                'https://github.com/synbiodex/pysbol3/thing2']
        collection.members = uris
        self.assertIn(sbol3.SBOL_MEMBER, collection._properties)
        self.assertNotIn(sbol3.SBOL_ORIENTATION, collection._properties)
        self.assertEqual(uris, collection.members)

    # Namespace testing
    def test_namespace_deduced(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        identity = posixpath.join(namespace, 'collection1')
        collection = sbol3.Collection(identity)
        self.assertEqual(namespace, collection.namespace)
        # Now test a namespace with a trailing #
        identity2 = f'{namespace}#collection2'
        collection2 = sbol3.Collection(identity2)
        self.assertEqual(namespace, collection2.namespace)

    def test_namespace_set(self):
        # Test that namespace is properly set on an object after
        # using set_namespace()
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        collection = sbol3.Collection('collection1')
        self.assertEqual(namespace, collection.namespace)

    def test_namespace_none(self):
        # Test the exception case when a namespace cannot be deduced
        identity = uuid.uuid4().urn
        collection = sbol3.Collection(identity)
        # The namespace should always be set per SBOL 3.0.1
        #  "A TopLevel object MUST have precisely one hasNamespace property"
        self.assertIsNotNone(collection.namespace)
        # There should be no validation errors on this object
        report = collection.validate()
        self.assertEqual(0, len(report))


class TestExperiment(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        experiment = sbol3.Experiment('experiment1')
        self.assertIsNotNone(experiment)
        self.assertEqual(0, len(experiment.members))
        self.assertEqual(sbol3.SBOL_EXPERIMENT, experiment.type_uri)

    def test_read(self):
        identity = 'https://github.com/synbiodex/pysbol3/experiment1'
        nt_data = f'<{identity}> <{rdflib.RDF.type}> <{sbol3.SBOL_EXPERIMENT}> .'
        doc = sbol3.Document()
        doc.read_string(nt_data, 'ttl')
        experiment = doc.find(identity)
        self.assertIsNotNone(experiment)
        self.assertIsInstance(experiment, sbol3.Collection)


if __name__ == '__main__':
    unittest.main()
