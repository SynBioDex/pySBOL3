import math

from . import *


class Identified(SBOLObject):
    def __init__(self) -> None:
        super().__init__()
        self.display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
        self.name = TextProperty(self, SBOL_NAME, 0, 1)
        self.description = TextProperty(self, SBOL_DESCRIPTION, 0, 1)
        self.derived_from = URIProperty(self, PROV_NS.wasDerivedFrom, 0, math.inf)
        self.generated_by = URIProperty(self, PROV_NS.wasGeneratedBy, 0, math.inf)
