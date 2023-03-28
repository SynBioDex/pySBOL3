import unittest

import sbol3


class TestFeature(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_valid(self):
        # should I create component first and add subcomponent into it???
        # Feature is abstract base class and hence it shouldn't be called directly, only their childs could?
        # Answer -> yes (for both questions)
        # 'this only works if we have subcomponent as a feature, so we need to generalize to all feature types'
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        ptet = sbol3.Component('pTetR', sbol3.SBO_DNA, roles=[sbol3.SO_PROMOTER])
        circuit = sbol3.Component('circuit', sbol3.SBO_DNA, roles=[sbol3.SO_ENGINEERED_REGION])
        ptet_sc = sbol3.SubComponent(ptet, orientation='https://identifiers.org/SO:0001030')
        # SO_FORWARD = 'https://identifiers.org/SO:0001030'
        circuit.features += [ptet_sc]
        report = ptet_sc.validate()
        self.assertEqual(0, len(report))

    def test_invalid(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        ptet = sbol3.Component('pTetR', sbol3.SBO_DNA, roles=[sbol3.SO_PROMOTER])
        circuit = sbol3.Component('circuit', sbol3.SBO_DNA, roles=[sbol3.SO_ENGINEERED_REGION])
        ptet_sc = sbol3.SubComponent(ptet, orientation='Wrong Orientation')  # not in the valid orientation list
        circuit.features += [ptet_sc]
        report = ptet_sc.validate()
        self.assertEqual(1, len(report))

    if __name__ == '__main__':
        unittest.main()
