from . import *


class ExperimentalData(TopLevel):

    def __init__(self, identity: str, *, type_uri: str = SBOL_EXPERIMENTAL_DATA):
        super().__init__(identity, type_uri)


Document.register_builder(SBOL_EXPERIMENTAL_DATA, ExperimentalData)
