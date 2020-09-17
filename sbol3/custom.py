import rdflib

from . import *


class CustomIdentified(Identified):

    def __init__(self, custom_type: str = None, *, name: str = None,
                 type_uri: str = SBOL_IDENTIFIED) -> None:
        super().__init__(name, type_uri)
        self.rdf_type = URIProperty(self, rdflib.RDF.type, 1, 1,
                                    initial_value=custom_type)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if self.rdf_type is None:
            raise ValidationError('rdf_type is a required property of CustomIdentified')


class CustomTopLevel(TopLevel):

    def __init__(self, name: str = None, custom_type: str = None,
                 *, type_uri: str = SBOL_TOP_LEVEL) -> None:
        super().__init__(name, type_uri)
        self.rdf_type = URIProperty(self, rdflib.RDF.type, 1, 1,
                                    initial_value=custom_type)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if self.rdf_type is None:
            raise ValidationError('rdf_type is a required property of CustomTopLevel')
