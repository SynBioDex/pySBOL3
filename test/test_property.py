import unittest

import rdflib

import sbol3


class TestProperty(unittest.TestCase):

    def test_slice_assignment(self):
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


if __name__ == '__main__':
    unittest.main()
