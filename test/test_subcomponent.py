import unittest

import sbol3


class TestSubComponent(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        instance_of = sbol3.Component('comp1', sbol3.SBO_DNA)
        sc1 = sbol3.SubComponent(instance_of)
        self.assertIsNotNone(sc1)
        self.assertEqual(instance_of.identity, sc1.instance_of)
        sc2 = sbol3.SubComponent(instance_of.identity)
        self.assertEqual(instance_of.identity, sc2.instance_of)

    def test_invalid_create(self):
        # SubComponent requires an `instance_of` argument
        sc = sbol3.SubComponent('')
        report = sc.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

    def test_external_instance_of(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/136
        c_uri = 'https://synbiohub.example.org/component1'
        m9_media = 'https://synbiohub.example.org/m9-media'
        e_coli = 'https://synbiohub.example.org/e-coli-DH5-alpha'
        c = sbol3.Component(c_uri, sbol3.SBO_DNA)
        sc1 = sbol3.SubComponent(m9_media)
        sc2 = sbol3.SubComponent(e_coli)
        c.features = [sc1, sc2]
        self.assertEqual(len(c.features), 2)
        doc1 = sbol3.Document()
        doc1.add(c)
        doc2 = sbol3.Document()
        doc2.read_string(doc1.write_string(sbol3.NTRIPLES),
                         sbol3.NTRIPLES)
        c2 = doc2.find(c_uri)
        self.assertIsNotNone(c2)
        self.assertEqual(2, len(c2.features))
        self.assertCountEqual([m9_media, e_coli],
                              [sc.instance_of for sc in c2.features])


if __name__ == '__main__':
    unittest.main()
