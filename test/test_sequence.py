import unittest

import sbol3


class TestSequence(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        self.assertEqual(display_id, seq.display_id)
        self.assertIsNone(seq.elements)
        self.assertIsNone(seq.encoding)

    def test_invalid(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        seq.elements = 'actg'
        with self.assertRaises(sbol3.ValidationError):
            seq.validate()

    def test_valid(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        seq.elements = 'actg'
        seq.encoding = sbol3.SBOL_IUPAC_DNA
        # Should not raise a ValidationError
        seq.validate()


if __name__ == '__main__':
    unittest.main()
