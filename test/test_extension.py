import unittest

from typing import Union

import sbol3

SAMPLE_SET_URI = 'http://bioprotocols.org/opil/v1#SampleSet'


class SampleSet(sbol3.CombinatorialDerivation, sbol3.CustomTopLevel):

    def __init__(self, identity: str, template: Union[sbol3.Component, str],
                 *, type_uri: str = SAMPLE_SET_URI):
        super().__init__(identity=identity, template=template,
                         type_uri=type_uri)
        # Add additional properties here


def build_sample_set(identity: str,
                     *, type_uri: str = SAMPLE_SET_URI):
    template = sbol3.PYSBOL3_MISSING
    return SampleSet(identity=identity, template=template, type_uri=type_uri)


sbol3.Document.register_builder(SAMPLE_SET_URI, build_sample_set)


class TestExtension(unittest.TestCase):

    def test_sample_set(self):
        # Test extending an SBOL class to create a new type with all the
        # properties of the SBOL type plus whatever other properties the
        # programmer defines. The key to doing this properly is to use
        # multiple inheritance to extend both the desired SBOL type and
        # CustomTopLevel so that the type is properly serialized to RDF.
        doc = sbol3.Document()
        ss_uri = 'http://example.org/sbol3/ss1'
        template_uri = 'http://example.org/sbol3/template1'
        ss = SampleSet(identity=ss_uri, template=template_uri)
        doc.add(ss)

        doc2 = sbol3.Document()
        rdf_format = sbol3.TURTLE
        output = doc.write_string(rdf_format)
        doc2.read_string(output, rdf_format)


if __name__ == '__main__':
    unittest.main()
