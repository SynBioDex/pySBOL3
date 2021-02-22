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
        seq.encoding = sbol3.SBOL_IUPAC_DNA
        # Should not raise a ValidationError
        seq.validate()

    def test_full_constructor(self):
        identity = 'https://github.com/synbiodex/pysbol3/s1'
        elements = 'GCAT'
        encoding = sbol3.SBOL_IUPAC_DNA
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


if __name__ == '__main__':
    unittest.main()
