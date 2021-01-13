from . import *


class Implementation(TopLevel):

    def __init__(self, identity: str, *, type_uri: str = SBOL_IMPLEMENTATION) -> None:
        super().__init__(identity, type_uri)
        self.built = ReferencedObject(self, SBOL_BUILT, 0, 1)
        self.validate()

    def validate(self) -> None:
        super().validate()


Document.register_builder(SBOL_IMPLEMENTATION, Implementation)
