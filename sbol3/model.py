from . import *


class Model(TopLevel):

    def __init__(self) -> None:
        super().__init__()
        self.source = URIProperty(self, SBOL_ROLE, 1, 1)
        self.language = URIProperty(self, SBOL_TYPE, 1, 1)
        self.framework = URIProperty(self, SBOL_SEQUENCES, 1, 1)
