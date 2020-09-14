import math
from typing import Union

from . import *


class Usage(Identified):

    def __init__(self, entity: str, *, name: str = None,
                 type_uri: str = PROV_USAGE) -> None:
        super().__init__(name, type_uri)
        self.entity = URIProperty(self, PROV_ENTITY, 1, 1,
                                  initial_value=entity)
        self.roles = URIProperty(self, PROV_ROLES, 0, math.inf)
        self.validate()


def build_usage(name: str, *, type_uri: str = PROV_USAGE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Usage(missing, name=name, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[PROV_ENTITY] = []
    return obj


Document.register_builder(PROV_USAGE, build_usage)


class Agent(TopLevel):

    def __init__(self, name: str, *, type_uri: str = PROV_AGENT) -> None:
        super().__init__(name, type_uri)
        self.validate()


Document.register_builder(PROV_AGENT, Agent)


class Plan(TopLevel):

    def __init__(self, name: str, *, type_uri: str = PROV_PLAN) -> None:
        super().__init__(name, type_uri)
        self.validate()


Document.register_builder(PROV_PLAN, Plan)


class Association(Identified):

    def __init__(self, agent: Union[str, Identified],
                 *, name: str = None,
                 type_uri: str = PROV_ASSOCIATION) -> None:
        super().__init__(name, type_uri)
        self.roles = URIProperty(self, PROV_ROLES, 0, math.inf)
        self.plan = ReferencedObject(self, PROV_PLANS, 0, 1)
        self.agent = ReferencedObject(self, PROV_AGENTS, 1, 1,
                                      initial_value=agent)
        self.validate()


def build_association(name: str, *, type_uri: str = PROV_USAGE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Association(missing, name=name, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[PROV_AGENTS] = []
    return obj


Document.register_builder(PROV_ASSOCIATION, build_association)


class Activity(TopLevel):

    def __init__(self, name: str, *, type_uri: str = PROV_ACTIVITY) -> None:
        super().__init__(name, type_uri)
        self.types = URIProperty(self, SBOL_TYPE, 0, math.inf)
        self.start_time = DateTimeProperty(self, PROV_STARTED_AT_TIME, 0, 1)
        self.end_time = DateTimeProperty(self, PROV_ENDED_AT_TIME, 0, 1)
        self.usage = OwnedObject(self, PROV_QUALIFIED_USAGE, 0, math.inf)
        self.association = OwnedObject(self, PROV_QUALIFIED_ASSOCIATION, 0, math.inf)
        self.validate()


Document.register_builder(PROV_ACTIVITY, Activity)
