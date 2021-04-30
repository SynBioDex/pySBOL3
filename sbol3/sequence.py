from typing import List, Any

from . import *


class Sequence(TopLevel):

    def __init__(self, identity: str, *,
                 elements: str = None, encoding: str = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None, generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_SEQUENCE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.elements = TextProperty(self, SBOL_ELEMENTS, 0, 1,
                                     initial_value=elements)
        self.encoding = URIProperty(self, SBOL_ENCODING, 0, 1,
                                    initial_value=encoding)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # If sequence is set, encoding is REQUIRED
        if self.elements and not self.encoding:
            message = 'Sequence encoding is required if elements are set'
            report.addError(self.identity, None, message)
        # Check that the encoding is part of the recommended set
        encodings = {
            IUPAC_DNA_ENCODING, IUPAC_RNA_ENCODING, IUPAC_PROTEIN_ENCODING,
            INCHI_ENCODING, SMILES_ENCODING
        }
        if self.encoding and self.encoding not in encodings:
            message = 'Sequence encoding is not in the recommended set'
            report.addWarning(self.identity, 'sbol3-10505', message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_sequence` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_sequence method
        :return: Whatever `visitor.visit_sequence` returns
        :rtype: Any

        """
        visitor.visit_sequence(self)


Document.register_builder(SBOL_SEQUENCE, Sequence)
