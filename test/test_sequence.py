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
        report = seq.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

    def test_valid(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        seq.elements = 'actg'
        seq.encoding = sbol3.IUPAC_DNA_ENCODING
        # Should not raise a ValidationError
        report = seq.validate()
        self.assertEqual(0, len(report))

    def test_full_constructor(self):
        identity = 'https://github.com/synbiodex/pysbol3/s1'
        elements = 'GCAT'
        encoding = sbol3.IUPAC_DNA_ENCODING
        attachments = ['https://github.com/synbiodex/pysbol3/attachment1']
        name = None
        description = None
        derived_from = ['https://github.com/synbiodex/pysbol3/parent1']
        generated_by = ['https://github.com/synbiodex/pysbol3/tool1']
        m1 = sbol3.Measure(value=2.3, unit='meter')
        measures = [m1]
        s1 = sbol3.Sequence(identity=identity,
                            elements=elements,
                            encoding=encoding,
                            attachments=attachments,
                            name=name,
                            description=description,
                            derived_from=derived_from,
                            generated_by=generated_by,
                            measures=measures)
        self.assertEqual(identity, s1.identity)
        self.assertEqual(elements, s1.elements)
        self.assertEqual(encoding, s1.encoding)
        self.assertEqual(attachments, s1.attachments)
        self.assertEqual(name, s1.name)
        self.assertEqual(description, s1.description)
        self.assertEqual(derived_from, s1.derived_from)
        self.assertEqual(generated_by, s1.generated_by)
        self.assertEqual(measures, s1.measures)

    def test_invalid_encoding(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'seq1'
        seq = sbol3.Sequence(display_id)
        self.assertIsNotNone(seq)
        seq.elements = 'actg'
        # This is an encoding from SBOL 3.0. It is no longer
        # valid as of 3.0.1/3.1.
        seq.encoding = 'http://sbols.org/v3#iupacNucleicAcid'
        # We expect 1 warning for the encoding that is not in the
        # recommended set.
        report = seq.validate()
        self.assertEqual(1, len(report))
        self.assertEqual(1, len(report.warnings))

    def test_initial_value(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/208
        identity = 'https://github.com/synbiodex/pysbol3/s1'
        elements = ''
        # encoding = sbol3.IUPAC_DNA_ENCODING
        s1 = sbol3.Sequence(identity=identity,
                            elements=elements)
        self.assertEqual(identity, s1.identity)
        self.assertEqual(elements, s1.elements)
        # self.assertEqual(encoding, s1.encoding)

    def test_generated_by(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        act1 = sbol3.Activity('act1')
        act2 = sbol3.Activity('act2')
        elements = 'acgt'
        seq1 = sbol3.Sequence(identity='seq1',
                              elements=elements)
        self.assertListEqual([], list(seq1.generated_by))
        # test a list of items
        activities = [act1, act2]
        seq2 = sbol3.Sequence(identity='seq2',
                              elements=elements,
                              generated_by=activities)
        self.assertListEqual([a.identity for a in activities],
                             list(seq2.generated_by))
        # test a singleton, which should gracefully be marshalled into a list
        activity = act1
        seq3 = sbol3.Sequence(identity='seq3',
                              elements=elements,
                              generated_by=activity)
        self.assertListEqual([activity.identity],
                             list(seq3.generated_by))


if __name__ == '__main__':
    unittest.main()
