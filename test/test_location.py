import unittest

import sbol3


class TestRange(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_creation(self):
        start = 1
        end = 10
        r = sbol3.Range(sbol3.PYSBOL3_MISSING, start, end)
        self.assertIsNotNone(r)
        self.assertEqual(start, r.start)
        self.assertEqual(end, r.end)

    def test_invalid_create(self):
        start = 0
        end = 10
        r = sbol3.Range(sbol3.PYSBOL3_MISSING, start, end)
        report = r.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

        # end must be > 0, and end must be > start
        start = 1
        end = 0
        r = sbol3.Range(sbol3.PYSBOL3_MISSING, start, end)
        report = r.validate()
        self.assertIsNotNone(report)
        self.assertEqual(2, len(report.errors))

        # end must be >= start
        start = 10
        end = 9
        r = sbol3.Range(sbol3.PYSBOL3_MISSING, start, end)
        report = r.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))

        start = 7
        end = 7
        r = sbol3.Range(sbol3.PYSBOL3_MISSING, start, end)
        self.assertEqual(start, r.start)
        self.assertEqual(end, r.end)
        report = r.validate()
        self.assertIsNotNone(report)
        self.assertEqual(0, len(report.errors))

    def test_keyword_args(self):
        # Test that all arguments, both required and optional, can be
        # specified by keyword
        seq_uri = 'https://example.com/pysbol3/seq1'
        start = 7
        end = 14
        range_uri = 'https://example.com/pysbol3/r1'
        r1 = sbol3.Range(seq_or_uri=seq_uri, end=end, start=start,
                         identity=range_uri)
        self.assertEqual(seq_uri, r1.sequence)
        self.assertEqual(start, r1.start)
        self.assertEqual(end, r1.end)
        self.assertEqual(range_uri, r1.identity)
        display_id = range_uri[range_uri.rindex('/') + 1:]
        self.assertEqual(display_id, r1.display_id)


class TestCut(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_creation(self):
        at = 1
        cut = sbol3.Cut(sbol3.PYSBOL3_MISSING, at)
        self.assertIsNotNone(cut)
        self.assertEqual(at, cut.at)
        at = 0
        cut = sbol3.Cut(sbol3.PYSBOL3_MISSING, at)
        self.assertIsNotNone(cut)
        self.assertEqual(at, cut.at)

    def test_invalid_create(self):
        # At must be >= 0
        at = -1
        cut = sbol3.Cut(sbol3.PYSBOL3_MISSING, at)
        report = cut.validate()
        self.assertIsNotNone(report)
        self.assertEqual(1, len(report.errors))


class TestEntireSequence(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_creation(self):
        # EntireSequence has no properties, so there isn't much to test here
        es = sbol3.EntireSequence(sbol3.PYSBOL3_MISSING)
        self.assertIsNotNone(es)


if __name__ == '__main__':
    unittest.main()
