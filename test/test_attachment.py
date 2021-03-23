import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestAttachment(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        base_url = 'https://github.com/SynBioDex/pySBOL3/'
        source_uri = base_url + 'blob/master/sbol3/attachment.py'
        att = sbol3.Attachment('attachment1', source_uri)
        self.assertEqual(source_uri, att.source)
        self.assertEqual(sbol3.SBOL_ATTACHMENT, att.type_uri)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'entity', 'attachment',
                                 'attachment.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        search_uri = 'https://sbolstandard.org/examples/attachment1'
        attachment = doc.find(search_uri)
        self.assertIsNotNone(attachment)
        self.assertIsInstance(attachment, sbol3.Attachment)
        self.assertEqual('https://sbolstandard.org/attachment1', attachment.source)
        self.assertEqual('https://identifiers.org/edam:format_2585', attachment.format)
        self.assertEqual(1000, attachment.size)
        self.assertEqual('aaa', attachment.hash)
        self.assertEqual('Alg1', attachment.hash_algorithm)


if __name__ == '__main__':
    unittest.main()
