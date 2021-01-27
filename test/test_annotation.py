import os
import tempfile
import unittest

import sbol3


class TestAnnotation(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_annotation(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Create custom annotation
        annotation_uri = 'http://example.org/boolean_property'
        annotation_value = 'foo'
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        c.annotation = sbol3.TextProperty(c, annotation_uri,
                                          0, 1, [])
        c.annotation = annotation_value
        self.assertEqual(annotation_value, c.annotation)

        doc = sbol3.Document()
        doc.add(c)
        doc2 = sbol3.Document()
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file = os.path.join(tmpdirname, 'annotation.xml')
            doc.write(test_file, sbol3.RDF_XML)
            # Roundtrip
            doc2.read(test_file, sbol3.RDF_XML)

        # Recover annotation
        c = doc2.find('c1')
        c.annotation = sbol3.TextProperty(c, annotation_uri,
                                          0, 1, [])
        self.assertEqual(annotation_value, c.annotation)


if __name__ == '__main__':
    unittest.main()
