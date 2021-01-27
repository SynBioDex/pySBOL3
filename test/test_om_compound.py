import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestUnitDivision(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Note, in practice we would use the already defined
        # http://www.ontology-of-units-of-measure.org/resource/om-2/kilometrePerHour
        display_id = 'udivision'
        symbol = 'k/hr'
        label = 'Kilometers per hour'
        numerator = 'http://www.ontology-of-units-of-measure.org/resource/om-2/kilometre'
        denominator = 'http://www.ontology-of-units-of-measure.org/resource/om-2/hour'
        udiv = sbol3.UnitDivision(display_id, symbol, label, numerator, denominator)
        self.assertIsNotNone(udiv)
        self.assertEqual(symbol, udiv.symbol)
        self.assertEqual(label, udiv.label)
        self.assertEqual(numerator, udiv.numerator)
        self.assertEqual(denominator, udiv.denominator)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'measurement_entity',
                                 'measurement', 'measurement.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        uri = 'https://sbolstandard.org/examples/millimolePerLitre'
        udiv = doc.find(uri)
        self.assertIsNotNone(udiv)
        self.assertIsInstance(udiv, sbol3.UnitDivision)
        self.assertEqual('https://sbolstandard.org/examples/millimole', udiv.numerator)
        self.assertEqual('https://sbolstandard.org/examples/litre', udiv.denominator)
        self.assertEqual('millimolar', udiv.name)
        self.assertEqual('millimolar', udiv.label)
        self.assertEqual('millimolePerLitre', udiv.display_id)


class TestUnitExponentiation(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Note, in practice we would use the already defined
        # http://www.ontology-of-units-of-measure.org/resource/om-2/cubicMetre
        display_id = 'uexponentiation'
        symbol = 'm3'
        label = 'cubic metre'
        base = 'http://www.ontology-of-units-of-measure.org/resource/om-2/metre'
        exponent = 3
        uexp = sbol3.UnitExponentiation(display_id, symbol, label, base, exponent)
        self.assertIsNotNone(uexp)
        self.assertEqual(symbol, uexp.symbol)
        self.assertEqual(label, uexp.label)
        self.assertEqual(base, uexp.base)
        self.assertEqual(exponent, uexp.exponent)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'measurement_entity',
                                 'measurement', 'measurement.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        uri = 'https://sbolstandard.org/examples/cubicMeter'
        uexp = doc.find(uri)
        self.assertIsNotNone(uexp)
        self.assertIsInstance(uexp, sbol3.UnitExponentiation)
        self.assertEqual('https://sbolstandard.org/examples/meter', uexp.base)
        self.assertEqual(3, uexp.exponent)
        self.assertEqual('cubicMeter', uexp.name)
        self.assertEqual('cubicMeter', uexp.label)
        self.assertEqual('cubicMeter', uexp.display_id)


class TestUnitMultiplication(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Note, in practice we would use the already defined
        # http://www.ontology-of-units-of-measure.org/resource/om-2/kelvinMole
        display_id = 'umultiplication'
        symbol = 'K mole'
        label = 'kelvin mole'
        term1 = 'https://sbolstandard.org/examples/kelvin'
        term2 = 'https://sbolstandard.org/examples/mole'
        umult = sbol3.UnitMultiplication(display_id, symbol, label, term1, term2)
        self.assertIsNotNone(umult)
        self.assertEqual(symbol, umult.symbol)
        self.assertEqual(label, umult.label)
        self.assertEqual(term1, umult.term1)
        self.assertEqual(term2, umult.term2)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'measurement_entity',
                                 'measurement', 'measurement.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        uri = 'https://sbolstandard.org/examples/kelvinMole'
        umult = doc.find(uri)
        self.assertIsNotNone(umult)
        self.assertIsInstance(umult, sbol3.UnitMultiplication)
        self.assertEqual('https://sbolstandard.org/examples/kelvin', umult.term1)
        self.assertEqual('https://sbolstandard.org/examples/mole', umult.term2)
        self.assertEqual('kelvinMole', umult.name)
        self.assertEqual('kelvinMole', umult.label)
        self.assertEqual('kelvinMole', umult.display_id)


if __name__ == '__main__':
    unittest.main()
