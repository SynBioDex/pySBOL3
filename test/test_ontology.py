import unittest
import sbol3

class TestOntology(unittest.TestCase):

    def test_SO(self):
        term_a = 'sequence_feature'
        uri = sbol3.SO.get_uri_by_term(term_a)
        self.assertEqual(uri, 'http://purl.obolibrary.org/obo/SO_0000110')
        term_b = sbol3.SO.get_term_by_uri(uri)
        self.assertEqual(term_a, term_b)
        with self.assertRaises(LookupError):
            uri = sbol3.SO.get_uri_by_term('not_a_term')
        term_a = 'sequence_feature'
        uri = sbol3.SO.get_uri_by_term(term_a)

    def test_SBO(self):
        uri_a = 'http://biomodels.net/SBO/SBO_0000000'
        term = sbol3.SBO.get_term_by_uri(uri_a)
        self.assertEqual(term, 'systems biology representation')
        uri_b = sbol3.SBO.get_uri_by_term(term)
        self.assertEqual(uri_a, uri_b)
        # self.assertEqual(uri, 'http://purl.obolibrary.org/obo/SO_0000110')

# term = sequence_ontology.get_term_by_uri('http://purl.obolibrary.org/obo/SO_0000014')
# print(term)
# print(uri)
# sequence_ontology.get_term_by_uri('foo')

if __name__ == '__main__':
    unittest.main()