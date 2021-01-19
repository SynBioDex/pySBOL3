import unittest

import rdflib

import sbol3


class TestCollection(unittest.TestCase):

    def test_create(self):
        collection = sbol3.Collection('collection1')
        self.assertIsNotNone(collection)
        self.assertEqual(0, len(collection.members))

    def test_read(self):
        identity = 'https://github.com/synbiodex/pysbol3/collection1'
        nt_data = f'<{identity}> <{rdflib.RDF.type}> <{sbol3.SBOL_COLLECTION}> .'
        doc = sbol3.Document()
        doc.read_string(nt_data, 'ttl')
        collection = doc.find(identity)
        self.assertIsNotNone(collection)
        self.assertIsInstance(collection, sbol3.Collection)

    def test_member_property(self):
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


class TestNamespace(unittest.TestCase):

    def test_create(self):
        namespace = sbol3.Namespace('namespace1')
        self.assertIsNotNone(namespace)
        self.assertEqual(0, len(namespace.members))

    def test_read(self):
        identity = 'https://github.com/synbiodex/pysbol3/namespace1'
        nt_data = f'<{identity}> <{rdflib.RDF.type}> <{sbol3.SBOL_NAMESPACE}> .'
        doc = sbol3.Document()
        doc.read_string(nt_data, 'ttl')
        namespace = doc.find(identity)
        self.assertIsNotNone(namespace)
        self.assertIsInstance(namespace, sbol3.Namespace)


class TestExperiment(unittest.TestCase):

    def test_create(self):
        experiment = sbol3.Experiment('experiment1')
        self.assertIsNotNone(experiment)
        self.assertEqual(0, len(experiment.members))

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
