import math

from . import *


class Collection(TopLevel):

    def __init__(self, name: str, *, type_uri: str = SBOL_COLLECTION) -> None:
        super().__init__(name, type_uri)
        self.members = ReferencedObject(self, SBOL_ORIENTATION, 0, math.inf)


class Namespace(Collection):

    def __init__(self, name: str, *, type_uri: str = SBOL_NAMESPACE) -> None:
        super().__init__(name, type_uri=type_uri)


class Experiment(Collection):

    def __init__(self, name: str, *, type_uri: str = SBOL_EXPERIMENT) -> None:
        super().__init__(name, type_uri=type_uri)


Document.register_builder(SBOL_COLLECTION, Collection)
Document.register_builder(SBOL_NAMESPACE, Namespace)
Document.register_builder(SBOL_EXPERIMENT, Experiment)