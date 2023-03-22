import unittest

import sbol3

class TestFeature(unittest.TestCase):
    
    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        # should I create component first and add subcomponent into it???
        # Feature is abstract base class and hence it shouldn't be called directly, only their childs could?

        # >>> ptet = sbol3.Component('pTetR', sbol3.SBO_DNA, roles=[sbol3.SO_PROMOTER])
        # >>> circuit = sbol3.Component('circuit', sbol3.SBO_DNA, roles=[sbol3.SO_ENGINEERED_REGION])
        # >>> ptet_sc = sbol3.SubComponent(ptet)
        # >>> circuit.features += [ptet_sc]

        # 'this only works if we have subcomponent as a feature, so we need to generalize to all feature types'
        ptet = sbol3.Component('pTetR', sbol3.SBO_DNA, roles=[sbol3.SO_PROMOTER])

        circuit = sbol3.Component('circuit', sbol3.SBO_DNA, roles=[sbol3.SO_ENGINEERED_REGION])

        ptet_sc = sbol3.SubComponent(ptet)
        circuit.features += [ptet_sc]
       
        # feature = sbol3.feature('feature1')
        self.assertIsNotNone(circuit.features)
        self.assertEqual(sbol3.SBOL_SUBCOMPONENT, ptet_sc.type_uri)

    def test_orientations(self):
        pass

    def test_roles(self):
        pass

    # def test_invalid(self):

    if __name__ == '__main__':
        unittest.main()