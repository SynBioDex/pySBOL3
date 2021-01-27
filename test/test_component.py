import unittest
from collections import Container

import sbol3


class TestComponent(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_roles(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        self.assertListEqual([], list(c.roles))
        self.assertEqual([], c.roles)
        c.roles = [sbol3.SO_PROMOTER]
        # Make sure the underlying datatype did not get overwritten
        self.assertNotIsInstance(c.roles, list)
        self.assertIsInstance(c.roles, Container)
        self.assertIn(sbol3.SO_PROMOTER, c.roles)
        self.assertEqual([sbol3.SO_PROMOTER], c.roles)
        self.assertTrue(c.roles == [sbol3.SO_PROMOTER])
        self.assertTrue([sbol3.SO_PROMOTER] == c.roles)
        # Other list manipulations
        c.roles.append(sbol3.SO_CDS)
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_CDS], c.roles)
        self.assertEqual([sbol3.SO_CDS], c.roles[1:])
        c.roles[1:] = [sbol3.SO_RBS]
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_RBS], c.roles)
        self.assertEqual([sbol3.SO_RBS], c.roles[1:])

    def test_features(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/149

        media_template_uri = 'https://sd2e.org/media_template'
        media_template = sbol3.LocalSubComponent(identity=media_template_uri,
                                                 types=[sbol3.SBO_FUNCTIONAL_ENTITY])
        media_template.name = 'media template'

        media_variable = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE)
        media_variable.variable = media_template

        all_sample_templates = [media_template]
        sample_template_uri = 'https://sd2e.org/measurement_template'
        sample_template = sbol3.Component(identity=sample_template_uri,
                                          component_type=sbol3.SBO_FUNCTIONAL_ENTITY)
        sample_template.name = 'measurement template'
        sample_template.features = all_sample_templates
        self.assertEqual(1, len(sample_template.features))
        self.assertEqual(media_template.identity,
                         sample_template.features[0].identity)


if __name__ == '__main__':
    unittest.main()
