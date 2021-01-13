from . import *


class Model(TopLevel):

    def __init__(self, identity: str, *, type_uri: str = SBOL_MODEL) -> None:
        super().__init__(identity, type_uri)
        self.source = URIProperty(self, SBOL_SOURCE, 1, 1)
        self.language = URIProperty(self, SBOL_LANGUAGE, 1, 1)
        self.framework = URIProperty(self, SBOL_FRAMEWORK, 1, 1)

    def validate(self) -> None:
        super().validate()
        # The source property is REQUIRED and MUST contain a URI reference (Section 6.8)
        if not self.source:
            msg = f'Model {self.identity} does not have a source'
            raise ValidationError(msg)
        # The language property is REQUIRED and MUST contain a URI (Section 6.8)
        if not self.language:
            msg = f'Model {self.identity} does not have a language'
            raise ValidationError(msg)
        # The framework property is REQUIRED and MUST contain a URI (Section 6.8)
        if not self.framework:
            msg = f'Model {self.identity} does not have a framework'
            raise ValidationError(msg)


Document.register_builder(SBOL_MODEL, Model)
