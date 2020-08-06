import logging
from typing import Dict, Callable, List, Optional

import rdflib

from . import *


class Document:

    uri_type_map: Dict[str, Callable] = {
        'http://sbols.org/v3#Model': Model,
        'http://sbols.org/v3#Component': Component
    }

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
                builder = Document.uri_type_map[str_o]
            except KeyError:
                # If we don't know how to build the type, it must be an extension.
                # Extensions do not have to comply with SBOL 3 type rules from
                # Identified on down. So we create them as SBOLObject instances
                self.logger.info(f'Creating generic object for type {str_o}')
                builder = SBOLObject
            obj = builder()
            obj.identity = str_s
            result[str_s] = obj
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
                obj.owned_objects[str_p] = other
            else:
                obj.properties[str_p].append(o)

    def clear(self) -> None:
        self.objects.clear()
        self.namespaces.clear()

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read(self, file_path, format='xml'):
        # TODO: clear the document, this isn't append
        graph = rdflib.Graph()
        with open(file_path, 'r') as infile:
            contents = infile.read()
        graph.parse(data=contents, format=format)
        objects = self._parse_objects(graph)
        self._parse_attributes(objects, graph)
        # Now what?
        # We've got the objects, now we need to store them within the document.
        # Also extract the namespaces from the graph.
        for prefix, uri in graph.namespaces():
            if not prefix:
                continue
            print(f'{prefix}: {uri}')
        # TODO: validate all objects
        for obj in objects.values():
            obj.validate()
        self.objects = [obj for uri, obj in objects.items()
                        if isinstance(obj, TopLevel)]
        self.namespaces = {prefix: uri for prefix, uri in graph.namespaces()
                           if prefix}

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
