from __future__ import annotations
import datetime
import math
from typing import Union, List, Any, Optional

from . import *
from .typing import uri_list, uri_singleton


class Usage(CustomIdentified):
    """How different entities are used in an prov:Activity is specified
    with the prov:Usage class, which is linked from an prov:Activity
    through the prov:Usage relationship. A prov:Usage is then linked
    to an prov:Entity through the prov:entity property URI and the
    prov:hadRole property species how the prov:Entity is used. When
    the prov:wasDerivedFrom property is used together with the full
    provenance described here, the entity pointed at by the
    prov:wasDerivedFrom property MUST be included in a prov:Usage.

    """

    def __init__(self, entity: str,
                 *, roles: Optional[str, list[str]] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = PROV_USAGE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.entity: uri_singleton = URIProperty(self, PROV_ENTITY, 1, 1,
                                                 initial_value=entity)
        self.roles: uri_list = URIProperty(self, PROV_ROLES, 0, math.inf,
                                           initial_value=roles)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_usage` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_usage method
        :return: Whatever `visitor.visit_usage` returns
        :rtype: Any

        """
        visitor.visit_usage(self)


def build_usage(identity: str, *, type_uri: str = PROV_USAGE) -> SBOLObject:
    obj = Usage(entity=PYSBOL3_MISSING, identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[PROV_ENTITY] = []
    return obj


Document.register_builder(PROV_USAGE, build_usage)


class Agent(CustomTopLevel):
    """Examples of agents are a person, organization, or software
    tool. These agents should be annotated with additional
    information, such as software version, needed to be able to run
    the same prov:Activity again.

    """

    def __init__(self, identity: str,
                 *, namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = PROV_AGENT) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_agent` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_agent method
        :return: Whatever `visitor.visit_agent` returns
        :rtype: Any

        """
        visitor.visit_agent(self)


Document.register_builder(PROV_AGENT, Agent)


class Plan(CustomTopLevel):
    """The prov:Plan entity can be used as a place holder to describe the
    steps (for example scripts or lab protocols) taken when an
    prov:Agent is used in a particular prov:Activity.

    """

    def __init__(self, identity: str,
                 *, namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = PROV_PLAN) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_plan` on `visitor` with `self` as the only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_plan method
        :return: Whatever `visitor.visit_plan` returns
        :rtype: Any
        """
        visitor.visit_plan(self)


Document.register_builder(PROV_PLAN, Plan)


class Association(CustomIdentified):
    """An prov:Association is linked to an prov:Agent through the
    prov:agent relationship. The prov:Association includes the
    prov:hadRole property to qualify the role of the prov:Agent in the
    prov:Activity.

    """

    def __init__(self, agent: Union[str, Identified],
                 *, roles: Optional[str, list[str]] = None,
                 plan: Union[Identified, str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = PROV_ASSOCIATION) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.roles: uri_list = URIProperty(self, PROV_ROLES, 0, math.inf,
                                           initial_value=roles)
        self.plan = ReferencedObject(self, PROV_PLANS, 0, 1,
                                     initial_value=plan)
        self.agent = ReferencedObject(self, PROV_AGENTS, 1, 1,
                                      initial_value=agent)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_association` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_association method
        :return: Whatever `visitor.visit_association` returns
        :rtype: Any

        """
        visitor.visit_association(self)


def build_association(identity: str,
                      *, type_uri: str = PROV_USAGE) -> SBOLObject:
    obj = Association(agent=PYSBOL3_MISSING, identity=identity,
                      type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[PROV_AGENTS] = []
    return obj


Document.register_builder(PROV_ASSOCIATION, build_association)


class Activity(CustomTopLevel):
    """A generated prov:Entity is linked through a prov:wasGeneratedBy
    relationship to an prov:Activity, which is used to describe how
    different prov:Agents and other entities were used. An
    prov:Activity is linked through a prov:qualifiedAssociation to
    prov:Associations, to describe the role of agents, and is linked
    through prov:qualifiedUsage to prov:Usages to describe the role of
    other entities used as part of the activity. Moreover, each
    prov:Activity includes optional prov:startedAtTime and
    prov:endedAtTime properties. When using prov:Activity to capture
    how an entity was derived, it is expected that any additional
    information needed will be attached as annotations. This may
    include software settings or textual notes. Activities can also be
    linked together using the prov:wasInformedBy relationship to
    provide dependency without explicitly specifying start and end
    times.

    """

    def __init__(self, identity: str,
                 *, types: Optional[str, list[str]] = None,
                 start_time: Union[str, datetime.datetime] = None,
                 end_time: Union[str, datetime.datetime] = None,
                 usage: List[Identified] = None,
                 association: List[Identified] = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = PROV_ACTIVITY) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.types: uri_list = URIProperty(self, SBOL_TYPE, 0, math.inf,
                                           initial_value=types)
        self.start_time = DateTimeProperty(self, PROV_STARTED_AT_TIME, 0, 1,
                                           initial_value=start_time)
        self.end_time = DateTimeProperty(self, PROV_ENDED_AT_TIME, 0, 1,
                                         initial_value=end_time)
        self.usage = OwnedObject(self, PROV_QUALIFIED_USAGE, 0, math.inf,
                                 initial_value=usage,
                                 type_constraint=Usage)
        self.association = OwnedObject(self, PROV_QUALIFIED_ASSOCIATION,
                                       0, math.inf,
                                       initial_value=association,
                                       type_constraint=Association)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_activity` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_activity method
        :return: Whatever `visitor.visit_activity` returns
        :rtype: Any

        """
        visitor.visit_activity(self)


Document.register_builder(PROV_ACTIVITY, Activity)
