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

    def test_dynamic_ontology_attributes(self):
        # Tests that our override of the __getattr__ method is working.
        # Tests dynamic generation of attributes for ontology terms; also verifies that
        # the Ontology's other methods (e.g., get_uri_by_term) remain accessible
        self.assertEqual(sbol3.SO.promoter, sbol3.SO.get_uri_by_term('promoter'))

        # When an Ontology term has spaces, the attribute that is dynamically generated
        # should replace these with underscores
        self.assertEqual(sbol3.SBO.systems_biology_representation,
                         sbol3.SBO.get_uri_by_term('systems biology representation'))

        self.assertNotEqual(sbol3.SBO.systems_biology_representation,
                            sbol3.SBO.reactant)

        # Raise an exception if an invalid term is specified
        with self.assertRaises(LookupError):
            not_a_term = sbol3.SO.not_a_term


if __name__ == '__main__':
    unittest.main()
