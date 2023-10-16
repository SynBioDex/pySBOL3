import unittest
from pathlib import Path

import sbol3


class TestVisitors(unittest.TestCase):

    def test_visitor_pattern(self):
        """Test that the visitor pattern is implemented and can use return values from visit functions"""
        class SumVisitor:
            def visit_document(self, doc: sbol3.Document):
                return sum(v.accept(self) for v in doc.objects)

            @staticmethod
            def visit_component(_: sbol3.Component):
                return 1

        doc = sbol3.Document()
        doc.read(Path(__file__).parent / 'resources' / 'circuit.nt')
        # File containing five Components and no other TopLevel objects
        self.assertEqual(doc.accept(SumVisitor()), 5)


if __name__ == '__main__':
    unittest.main()
