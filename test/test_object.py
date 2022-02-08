import posixpath
import unittest

import sbol3


class TestObject(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_trailing_slash(self):
        # A trailing slash on an object's identity should automatically be removed
        sbol3.set_namespace('http://example.org/sbol3')
        slash_identity = posixpath.join(sbol3.get_namespace(), 'c1', '')
        self.assertTrue(slash_identity.endswith(posixpath.sep))
        c = sbol3.Component(slash_identity, sbol3.SBO_DNA)
        identity = slash_identity.strip(posixpath.sep)
        self.assertEqual(identity, c.identity)

    def test_copy_properties(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        root = sbol3.Component('root', sbol3.SBO_DNA)
        root.name = 'foo'
        objects = sbol3.copy([root])
        root_copy = objects[0]
        self.assertEqual(root_copy.name, 'foo')

    def test_copy_child_objects(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        root = sbol3.Component('root', sbol3.SBO_DNA)
        sub1 = sbol3.Component('sub1', sbol3.SBO_DNA)
        sub2 = sbol3.Component('sub2', sbol3.SBO_DNA)
        sc1 = sbol3.SubComponent(sub1)
        sc2 = sbol3.SubComponent(sub2)
        root.features.append(sc1)
        root.features.append(sc2)
        doc.add(root)
        doc.add(sub1)
        doc.add(sub2)

        doc2 = sbol3.Document()
        objects = sbol3.copy([root], into_document=doc2)
        root_copy = objects[0]
        self.assertIn(root_copy, doc2.objects)
        self.assertEqual([sc.identity for sc in root.features],
                         [sc.identity for sc in root_copy.features])

    def test_replace_namespace(self):
        # Verify that replace_namespace is not exported from sbol3
        self.assertNotIn('replace_namespace', dir(sbol3))
        # replace_namespace should raise NotImplmentedError
        # See https://github.com/SynBioDex/pySBOL3/issues/132
        with self.assertRaises(NotImplementedError):
            from sbol3.object import replace_namespace
            replace_namespace(None, None, None)

    def test_copy_is_deprecated(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        name = 'ed1'
        ed1 = sbol3.ExternallyDefined(types=[sbol3.SBO_DNA],
                                      definition='https://example.org/other')
        with self.assertWarns(DeprecationWarning):
            ed1.copy()


if __name__ == '__main__':
    unittest.main()
