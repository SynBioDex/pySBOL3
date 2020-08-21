import logging
from typing import Dict, Callable, List, Optional

import rdflib

from . import *


class Document:

    @staticmethod
    def register_builder(type_uri: str,
                         builder: Callable[[str, str], SBOLObject]) -> None:
        """A builder function will be called with an identity and a keyword argument type_uri.

        builder(identity_uri: str, type_uri: str = None) -> SBOLObject
        """
        Document._uri_type_map[type_uri] = builder

    # Map type URIs to a builder function to construct entities from
    # RDF triples.
    _uri_type_map: Dict[str, Callable[[str, str], SBOLObject]] = {}

    def __init__(self):
        self.logger = logging.getLogger(SBOL_LOGGER_NAME)
        self.objects: List[Identified] = []
        self.namespaces: Dict[str, str] = {}

    def _parse_objects(self, graph):
        result = {}
        for s, p, o in graph.triples((None, rdflib.RDF.type, None)):
            str_o = str(o)
            str_s = str(s)
            try:
                builder = Document._uri_type_map[str_o]
            except KeyError:
                # If we don't know how to build the type, it must be an extension.
                # Extensions do not have to comply with SBOL 3 type rules from
                # Identified on down. So we create them as SBOLObject instances
                self.logger.info(f'Creating generic object for type {str_o}')
                builder = SBOLObject
            obj = builder(str_s, type_uri=str_o)
            obj.document = self
            result[obj.identity] = obj
        return result

    @staticmethod
    def _parse_attributes(objects, graph):
        for s, p, o in graph.triples((None, None, None)):
            if p == rdflib.RDF.type:
                # RDF.types have been processed already
                continue
            str_s = str(s)
            str_p = str(p)
            obj = objects[str_s]
            if str_p in obj.owned_objects:
                other_identity = str(o)
                other = objects[other_identity]
                obj.owned_objects[str_p].append(other)
            else:
                obj.properties[str_p].append(o)

    @staticmethod
    def _clean_up_singletons(objects: Dict[str, SBOLObject]):
        """Clean up singleton properties after reading an SBOL file.

        When an SBOL file is read, values are appended to the property
        stores without knowledge of which stores are singletons and
        which stores are lists. This method cleans up singleton properties
        by ensuring that each has exactly one value.
        """
        # This is necessary due to defaulting of properties when using
        # the builder. Some objects have required properties, which the
        # builder sets. In the case of singleton values, that can result
        # in multiple values in a singleton property. Only the first value
        # is used, so the value read from file is ignored.
        for _, obj in objects.items():
            for name, attr in obj.__dict__.items():
                if isinstance(attr, SingletonProperty):
                    prop_uri = attr.property_uri
                    store = attr._storage()
                    if len(store[prop_uri]) > 1:
                        store[prop_uri] = store[prop_uri][-1:]

    def clear(self) -> None:
        self.objects.clear()
        self.namespaces.clear()

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read(self, file_path, format='xml') -> None:
        with open(file_path, 'r') as infile:
            contents = infile.read()
        return self.read_string(contents, format)

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read_string(self, data: str, format: str = 'xml') -> None:
        # TODO: clear the document, this isn't append
        graph = rdflib.Graph()
        graph.parse(data=data, format=format)
        objects = self._parse_objects(graph)
        self._parse_attributes(objects, graph)
        self._clean_up_singletons(objects)
        # Validate all the objects
        for obj in objects.values():
            obj.validate()
        # Store the TopLevel objects in the Document
        self.objects = [obj for uri, obj in objects.items()
                        if isinstance(obj, TopLevel)]
        # Store the namespaces in the Document for later use
        self.namespaces = {prefix: uri for prefix, uri in graph.namespaces()
                           if prefix}

    def add(self, obj: TopLevel) -> None:
        """Add objects to the document.
        """
        if isinstance(obj, TopLevel):
            self.objects.append(obj)
            obj.document = self
        else:
            message = f'Expected TopLevel instance, {type(obj).__name__} found'
            raise TypeError(message)

    def _find_in_objects(self, search_string: str) -> Optional[Identified]:
        # TODO: implement recursive search
        for obj in self.objects:
            # TODO: needs an object.find(search_string) method on ... Identified?
            pass
        return None

    def find(self, search_string: str) -> Optional[Identified]:
        # Search string might be a URI or an id like display_id
        # TODO: should we check `name` as well?
        for obj in self.objects:
            if obj.identity == search_string:
                return obj
            if obj.display_id and obj.display_id == search_string:
                return obj
        return self._find_in_objects(search_string)

    def write(self, path: str, file_format='xml') -> None:
        graph = rdflib.Graph()
        for obj in self.objects:
            obj.serialize(graph)
        graph.serialize(path, format=file_format)
