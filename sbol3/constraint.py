from . import *


class Constraint(Identified):

    def __init__(self, name: str, *, type_uri: str = SBOL_CONSTRAINT) -> None:
        super().__init__(name, type_uri)
        self.restriction = URIProperty(self, SBOL_RESTRICTION, 1, 1)
        self.subject = ReferencedObject(self, SBOL_SUBJECT, 1, 1)
        self.object = ReferencedObject(self, SBOL_OBJECT, 1, 1)

    def validate(self) -> None:
        super().validate()


Document.register_builder(SBOL_CONSTRAINT, Constraint)
