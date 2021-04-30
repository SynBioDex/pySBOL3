from typing import List, Any

from . import *


class ExperimentalData(TopLevel):
    """The purpose of the ExperimentalData class is to aggregate links to
    experimental data files. An ExperimentalData is typically
    associated with a single sample, lab instrument, or experimental
    condition and can be used to describe the output of the test phase
    of a design-build-test-learn workflow.

    """

    def __init__(self, identity: str,
                 *, namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_EXPERIMENTAL_DATA):
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_experimental_data` on `visitor` with `self` as the
        only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_experimental_data
                                method
        :return: Whatever `visitor.visit_experimental_data` returns
        :rtype: Any

        """
        visitor.visit_experimental_data(self)


Document.register_builder(SBOL_EXPERIMENTAL_DATA, ExperimentalData)
