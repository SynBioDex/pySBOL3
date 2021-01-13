import math
import posixpath
from typing import Union
from urllib.parse import urlparse

import rdflib

from . import *


class Identified(SBOLObject):

    def __init__(self, identity: str, type_uri: str) -> None:
        super().__init__(identity, type_uri)
        self._display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
        self.name = TextProperty(self, SBOL_NAME, 0, 1)
        self.description = TextProperty(self, SBOL_DESCRIPTION, 0, 1)
        self.derived_from = URIProperty(self, PROV_DERIVED_FROM, 0, math.inf)
        self.generated_by = URIProperty(self, PROV_GENERATED_BY, 0, math.inf)
        # The type_constraint for measures should really be Measure but
        # that's a circular dependency. Instead we make the type constraint
        # Identified to constrain it somewhat. Identified is the best we
        # can do since every other SBOL class requires Identified to be defined.
        self.measures = OwnedObject(self, SBOL_HAS_MEASURE, 0, math.inf,
                                    type_constraint=Identified)
        # Identity has been set by the SBOLObject constructor
        self._display_id = self._extract_display_id(self.identity)

    @staticmethod
    def _is_valid_display_id(display_id: str) -> bool:
        if display_id is None:
            return True
        # A display id [...] value MUST be composed of only alphanumeric
        # or underscore characters and MUST NOT begin with a digit.
        # (Section 6.1)
        #
        # Make sure everything other than underscores are alphanumeric, and
        # make sure the first character is not a digit.
        #
        # Note: This implies that '_' is not a valid displayId because `isalnum()`
        # will return false if the string is empty, which it will be after we filter
        # out the lone underscore.
        return display_id.replace('_', '').isalnum() and not display_id[0].isdigit()

    @staticmethod
    def _extract_display_id(identity: str) -> Union[None, str]:
        if not identity:
            return None
        parsed = urlparse(identity)
        if not (parsed.scheme and parsed.netloc and parsed.path):
            # if the identity is not a URL, we cannot extract a display id
            # and display id is optional in this case
            return None
        display_id = parsed.path.split('/')[-1]
        if Identified._is_valid_display_id(display_id):
            return display_id
        else:
            msg = f'"{display_id}" is not a valid displayId.'
            msg += ' A displayId MUST be composed of only alphanumeric'
            msg += ' or underscore characters and MUST NOT begin with a digit.'
            raise ValueError(msg)

    def _validate_display_id(self) -> None:
        if self.identity_is_url():
            if (self.display_id is not None and
                    Identified._is_valid_display_id(self.display_id) and
                    self.identity.endswith(self.display_id)):
                return
        else:
            if Identified._is_valid_display_id(self.display_id):
                return
        message = f'{self.display_id} is not a valid displayId for {self.identity}'
        raise ValidationError(message)

    def _update_identity(self, identity: str, display_id: str) -> None:
        """Updates the identity of an Identified when it is added to a
        parent object. SBOL compliant objects and URIs require updating
        whenever an owned object is added to a new parent.
        """
        self._identity = identity
        self._display_id = display_id
        # Now cycle through any owned objects and update their identities
        for _, objects in self._owned_objects.items():
            for child in objects:
                if child.display_id:
                    new_display_id = child.display_id
                else:
                    # Generate a display id based on type and number
                    type_name = child.type_uri[len(SBOL3_NS):]
                    counter_value = self.counter_value(type_name)
                    new_display_id = f'{type_name}{counter_value}'
                new_identity = posixpath.join(self.identity, new_display_id)
                child._update_identity(new_identity, new_display_id)

    def counter_value(self, type_name: str):
        result = 0
        for _, objects in self._owned_objects.items():
            for sibling in objects:
                if sibling.display_id and sibling.display_id.startswith(type_name):
                    counter_string = sibling.display_id[len(type_name):]
                    counter_int = int(counter_string)
                    if counter_int > result:
                        result = counter_int
        return result + 1

    @property
    def display_id(self):
        # display_id is a read only property
        return self._display_id

    def validate(self) -> None:
        super().validate()
        self._validate_display_id()

    def serialize(self, graph: rdflib.Graph):
        identity = rdflib.URIRef(self.identity)
        graph.add((identity, rdflib.RDF.type, rdflib.URIRef(self.type_uri)))
        for prop, items in self._properties.items():
            if not items:
                continue
            rdf_prop = rdflib.URIRef(prop)
            for item in items:
                graph.add((identity, rdf_prop, item))
        for prop, items in self._owned_objects.items():
            if not items:
                continue
            rdf_prop = rdflib.URIRef(prop)
            for item in items:
                graph.add((identity, rdf_prop, rdflib.URIRef(item.identity)))
                item.serialize(graph)
