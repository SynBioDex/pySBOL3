from . import *


class Attachment(TopLevel):

    def __init__(self, identity: str, source: str,
                 *, type_uri: str = SBOL_ATTACHMENT):
        super().__init__(identity, type_uri)
        self.source = URIProperty(self, SBOL_SOURCE, 1, 1,
                                  initial_value=source)
        self.format = URIProperty(self, SBOL_FORMAT, 0, 1)
        self.size = IntProperty(self, SBOL_SIZE, 0, 1)
        self.hash = TextProperty(self, SBOL_HASH, 0, 1)
        self.hash_algorithm = TextProperty(self, SBOL_HASH_ALGORITHM, 0, 1)
        self.validate()

    def validate(self) -> None:
        super().validate()
        # An Attachment must have 1 source
        if self.source is None:
            message = f'Attachment {self.identity} must have a source'
            raise ValidationError(message)


def build_attachment(identity: str, *, type_uri: str = SBOL_COMPONENT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Attachment(identity, missing, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_SOURCE] = []
    return obj


Document.register_builder(SBOL_ATTACHMENT, build_attachment)
