import unittest

import sbol3


class TestFeature(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_valid(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        ptet = sbol3.Component('pTetR', sbol3.SBO_DNA, roles=[sbol3.SO_PROMOTER])
        circuit = sbol3.Component('circuit', sbol3.SBO_DNA, roles=[sbol3.SO_ENGINEERED_REGION])
        ptet_sc = sbol3.SubComponent(ptet, orientation=sbol3.SO_FORWARD)
        circuit.features += [ptet_sc]
        report = ptet_sc.validate()
        self.assertEqual(0, len(report))

    def test_invalid(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        ptet = sbol3.Component('pTetR', sbol3.SBO_DNA, roles=[sbol3.SO_PROMOTER])
        circuit = sbol3.Component('circuit', sbol3.SBO_DNA, roles=[sbol3.SO_ENGINEERED_REGION])
        # orientation should be an item from this list [SO_FORWARD, SO_REVERSE, SBOL_INLINE, SBOL_REVERSE_COMPLEMENT]
        ptet_sc = sbol3.SubComponent(ptet, orientation='Wrong Orientation')
        circuit.features += [ptet_sc]
        report = ptet_sc.validate()
        self.assertEqual(1, len(report))

    if __name__ == '__main__':
        unittest.main()
