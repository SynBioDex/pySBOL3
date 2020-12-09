import posixpath
import unittest

import sbol3


class TestObject(unittest.TestCase):

    def setUp(self) -> None:
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
        doc = sbol3.Document()
        root = sbol3.Component('root', sbol3.SBO_DNA)
        root.name = 'foo'
        root_copy = root.copy()
        self.assertEqual(root_copy.name, 'foo')

    def test_copy_child_objects(self):
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
        root_copy = root.copy(target_doc=doc2)
        self.assertEqual([sc.identity for sc in root.features],
                         [sc.identity for sc in root_copy.features])


if __name__ == '__main__':
    unittest.main()
