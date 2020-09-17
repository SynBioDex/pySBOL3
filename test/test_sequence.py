import unittest

import sbol3


class TestSequence(unittest.TestCase):

    def test_create(self):
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        self.assertEqual(display_id, seq.display_id)
        self.assertIsNone(seq.elements)
        self.assertIsNone(seq.encoding)

    def test_invalid(self):
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        seq.elements = 'actg'
        with self.assertRaises(sbol3.ValidationError):
            seq.validate()

    def test_valid(self):
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        seq.elements = 'actg'
        seq.encoding = sbol3.SBOL_IUPAC_DNA
        # Should not raise a ValidationError
        seq.validate()


if __name__ == '__main__':
    unittest.main()
