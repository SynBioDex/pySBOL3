from __future__ import annotations
import abc
import math
from typing import List, Optional

from . import *

from .typing import *


class Feature(Identified, abc.ABC):
    """Feature is an abstract base class."""

    def __init__(self, identity: str, type_uri: str,
                 *, roles: Optional[str, list[str]] = None,
                 orientation: Optional[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None) -> None:
        super().__init__(identity=identity, type_uri=type_uri, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.roles: uri_list = URIProperty(self, SBOL_ROLE, 0, math.inf,
                                           initial_value=roles)
        self.orientation: uri_singleton = URIProperty(self, SBOL_ORIENTATION, 0, 1,
                                                      initial_value=orientation)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # If there is an orientation, it must be in the valid set
        if self.orientation is not None:
            valid_orientations = [SO_FORWARD, SO_REVERSE,
                                  SBOL_INLINE, SBOL_REVERSE_COMPLEMENT]
            if self.orientation not in valid_orientations:
                message = f'{self.orientation} is not a valid orientation'
                report.addError(self.identity, None, message)
        return report
