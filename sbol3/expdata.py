from . import *


class ExperimentalData(TopLevel):

    def __init__(self, name: str, *, type_uri: str = SBOL_EXPERIMENTAL_DATA):
        super().__init__(name, type_uri)


Document.register_builder(SBOL_EXPERIMENTAL_DATA, ExperimentalData)
