import math

from . import *


class Identified(SBOLObject):
    def __init__(self) -> None:
        super().__init__()
        # Does this need to be a property? It does not get serialized to the RDF file.
        # Could it be an attribute that gets composed on the fly?
        self.identity = ''
        self.display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
        self.name = TextProperty(self, SBOL_NAME, 0, 1)
        self.description = TextProperty(self, SBOL_DESCRIPTION, 0, 1)
        self.derived_from = URIProperty(self, PROV_DERIVED_FROM, 0, math.inf)
        self.generated_by = URIProperty(self, PROV_GENERATED_BY, 0, math.inf)
