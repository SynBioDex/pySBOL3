import math

from . import *
from .typing import *


class Participation(Identified):

    def __init__(self, roles: List[str],
                 participant: Union[SBOLObject, str],
                 *, identity: str = None,
                 type_uri: str = SBOL_PARTCIPATION) -> None:
        super().__init__(identity, type_uri)
        self.roles: uri_list = URIProperty(self, SBOL_ROLE, 1, math.inf,
                                           initial_value=roles)
        self.participant = ReferencedObject(self, SBOL_PARTICIPANT, 1, 1,
                                            initial_value=participant)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if len(self.roles) < 1:
            raise ValidationError('Participation must have at least one role')
        if self.participant is None:
            raise ValidationError('Participation must have a participant')


def build_participation(identity: str,
                        *, type_uri: str = SBOL_PARTCIPATION) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Participation([missing], missing, identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_ROLE] = []
    obj._properties[SBOL_PARTICIPANT] = []
    return obj


Document.register_builder(SBOL_PARTCIPATION, build_participation)
