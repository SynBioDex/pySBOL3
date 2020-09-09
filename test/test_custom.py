import unittest

import rdflib

import sbol3


class TestCustomTopLevel(unittest.TestCase):

    def test_create(self):
        custom_type = 'https://github.com/synbiodex/pysbol3/CustomType'
        ctl = sbol3.CustomTopLevel('custom1', custom_type)
        # Go behind the scenes to verify
        self.assertEqual(rdflib.URIRef(custom_type),
                         ctl._properties[rdflib.RDF.type][0])

    # TODO: We really want to verify the serialization of the custom top
    #       level as well. There is no Document.writeString() yet.


class TestCustomIdentified(unittest.TestCase):

    def test_create(self):
        custom_type = 'https://github.com/synbiodex/pysbol3/CustomType'
        ctl = sbol3.CustomIdentified(name='custom1',
                                     custom_type=custom_type)
        # Go behind the scenes to verify
        self.assertEqual(rdflib.URIRef(custom_type),
                         ctl._properties[rdflib.RDF.type][0])

    # TODO: We really want to verify the serialization of the custom
    #       identified as well. We need to attach it to a top level
    #       to see that work.


if __name__ == '__main__':
    unittest.main()
