import unittest

import rdflib

import sbol3


class TestInteraction(unittest.TestCase):

    def test_create(self):
        display_id = 'interaction1'
        types = [sbol3.SBO_INHIBITION]
        interaction = sbol3.Interaction(display_id, types)
        self.assertIsNotNone(interaction)
        self.assertEqual(display_id, interaction.display_id)
        self.assertEqual(types, interaction.types)

    def test_read(self):
        component_id = 'https://github.com/synbiodex/pysbol3/component1'
        interaction_id = 'https://github.com/synbiodex/pysbol3/interaction1'
        rdf_type = rdflib.RDF.type
        nt_data = f'<{component_id}> <{rdf_type}> <{sbol3.SBOL_COMPONENT}> .\n'
        nt_data += f'<{component_id}> <{sbol3.SBOL_TYPE}> <{sbol3.SBO_DNA}> .\n'
        nt_data += f'<{component_id}> <{sbol3.SBOL_INTERACTIONS}> <{interaction_id}> .\n'
        nt_data += f'<{interaction_id}> <{rdf_type}> <{sbol3.SBOL_INTERACTION}> .\n'
        nt_data += f'<{interaction_id}> <{sbol3.SBOL_TYPE}> <{sbol3.SBO_INHIBITION}> .\n'
        doc = sbol3.Document()
        doc.read_string(nt_data, 'ttl')
        component = doc.find(component_id)
        self.assertIsNotNone(component)
        self.assertIsInstance(component, sbol3.Component)
        interaction = component.interactions[0]
        self.assertEqual(interaction_id, interaction.identity)
        self.assertEqual([sbol3.SBO_INHIBITION], interaction.types)


if __name__ == '__main__':
    unittest.main()
