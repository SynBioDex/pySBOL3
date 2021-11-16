from typing import List, Any, Optional

from . import *


class Attachment(TopLevel):
    """The purpose of the Attachment class is to serve as a general
    container for data files, especially experimental data files. It
    provides a means for linking files and metadata to SBOL designs.

    """

    def __init__(self, identity: str, source: str,
                 *, format: Optional[str] = None,
                 size: int = None,
                 hash: str = None, hash_algorithm: str = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_ATTACHMENT):
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.source = URIProperty(self, SBOL_SOURCE, 1, 1,
                                  initial_value=source)
        self.format = URIProperty(self, SBOL_FORMAT, 0, 1,
                                  initial_value=format)
        self.size = IntProperty(self, SBOL_SIZE, 0, 1,
                                initial_value=size)
        self.hash = TextProperty(self, SBOL_HASH, 0, 1,
                                 initial_value=hash)
        self.hash_algorithm = TextProperty(self, SBOL_HASH_ALGORITHM, 0, 1,
                                           initial_value=hash_algorithm)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # An Attachment must have 1 source
        if self.source is None:
            message = f'Attachment {self.identity} must have a source'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_attachment` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_attachment method
        :return: Whatever `visitor.visit_attachment` returns
        :rtype: Any

        """
        visitor.visit_attachment(self)


def build_attachment(identity: str,
                     *, type_uri: str = SBOL_COMPONENT) -> SBOLObject:
    obj = Attachment(identity=identity, source=PYSBOL3_MISSING,
                     type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_SOURCE] = []
    return obj


Document.register_builder(SBOL_ATTACHMENT, build_attachment)
