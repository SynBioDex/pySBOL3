import math
import posixpath
from typing import Union, List, Callable, Any
from urllib.parse import urlparse

import rdflib

from . import *
from .utils import parse_class_name


class Identified(SBOLObject):
    """All SBOL-defined classes are directly or indirectly derived from
    the Identified abstract class. This inheritance means that all
    SBOL objects are uniquely identified using URIs that uniquely
    refer to these objects within an SBOL document or at locations on
    the World Wide Web.

    """

    def __init__(self, identity: str, type_uri: str,
                 *, name: str = None, description: str = None,
                 derived_from: List[str] = None, generated_by: List[str] = None,
                 measures: List[SBOLObject] = None) -> None:
        super().__init__(identity)
        self._document = None
        self._display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
        self.name = TextProperty(self, SBOL_NAME, 0, 1, initial_value=name)
        self.description = TextProperty(self, SBOL_DESCRIPTION, 0, 1,
                                        initial_value=description)
        self.derived_from = URIProperty(self, PROV_DERIVED_FROM, 0, math.inf,
                                        initial_value=derived_from)
        self.generated_by = ReferencedObject(self, PROV_GENERATED_BY, 0, math.inf,
                                             initial_value=generated_by)
        # The type_constraint for measures should really be Measure but
        # that's a circular dependency. Instead we make the type constraint
        # Identified to constrain it somewhat. Identified is the best we
        # can do since every other SBOL class requires Identified to be defined.
        self.measures = OwnedObject(self, SBOL_HAS_MEASURE, 0, math.inf,
                                    initial_value=measures,
                                    type_constraint=Identified)
        # Identity has been set by the SBOLObject constructor
        self._display_id = self._extract_display_id(self.identity)
        self._rdf_types = URIProperty(self, RDF_TYPE, 1, math.inf,
                                      initial_value=[type_uri])

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

    @property
    def type_uri(self):
        return self._rdf_types[0]

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value
        # Now assign document to the whole object hierarchy
        # rooted here
        # Note: we prevent an infinite loop by assigning to
        # `_document` instead of recursively entering this
        # method by assigning to `document`.

        def assign_document(x: Identified):
            x._document = value
        self.traverse(assign_document)

    def _validate_display_id(self, report: ValidationReport) -> None:
        if self.identity_is_url():
            if (self.display_id is not None and
                    Identified._is_valid_display_id(self.display_id) and
                    self.identity.endswith(self.display_id)):
                return
        else:
            if Identified._is_valid_display_id(self.display_id):
                return
        message = f'{self.display_id} is not a valid displayId for {self.identity}'
        report.addError(self.identity, None, message)

    def _update_identity(self, identity: str, display_id: str) -> None:
        """Updates the identity of an Identified when it is added to a
        parent object. SBOL compliant objects and URIs require updating
        whenever an owned object is added to a new parent.
        """
        if self._identity is not None:
            class_name = type(self).__name__
            msg = f'{class_name} already has identity {self.identity}'
            msg += ' and cannot be re-parented.'
            raise ValueError(msg)
        self._identity = identity
        self._display_id = display_id
        # Now cycle through any owned objects and update their identities
        for _, objects in self._owned_objects.items():
            for child in objects:
                if child.display_id:
                    new_display_id = child.display_id
                else:
                    # Generate a display id based on type and number
                    type_name = parse_class_name(child.type_uri)
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

    @property
    def properties(self):
        return list(self._properties.keys())

    def clear_property(self, uri):
        """Clears the internal storage of a property based on the URI.
        This is for advanced usage only, and may cause inconsistent
        objects and/or graphs.

        USE WITH CARE.
        """
        # If the URI is not in _properties or _owned_objects
        # silently do nothing. This is for advanced usage, so
        # don't tell the user it wasn't there.
        if uri in self._properties:
            self._properties[uri] = []
        elif uri in self._owned_objects:
            self._owned_objects[uri] = []

    def _validate_properties(self, report: ValidationReport) -> None:
        """Call validate on all the properties. Pass the name of the
        property so the error message is more friendly.
        """
        for k, v in self.__dict__.items():
            if isinstance(v, Property):
                v.validate(k, report)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        if report is None:
            report = ValidationReport()
        # Do validations for Identified
        self._validate_display_id(report)
        self._validate_properties(report)
        # Validate all owned objects
        for object_list in self._owned_objects.values():
            for obj in object_list:
                obj.validate(report)
        return report

    def serialize(self, graph: rdflib.Graph):
        identity = rdflib.URIRef(self.identity)
        # graph.add((identity, rdflib.RDF.type, rdflib.URIRef(self.type_uri)))
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

    def accept(self, visitor: Any) -> Any:
        message = f'accept is not implemented for {type(self).__qualname__}'
        raise NotImplementedError(message)

    def traverse(self, func: Callable[['Identified'], None]):
        """Enable a traversal of this object and all of its children by
        invoking the passed function on all objects.
        """
        # Call the function on the children first, then self.
        for object_list in self._owned_objects.values():
            for obj in object_list:
                obj.traverse(func)
        func(self)
