import logging
from typing import Dict, Callable

import rdflib

from . import *


class Document:

    uri_type_map: Dict[str, Callable] = {
        'http://sbols.org/v3#Model': Model,
        'http://sbols.org/v3#Component': Component
    }

    def __init__(self):
        self.logger = logging.getLogger(SBOL_LOGGER_NAME)

    def _parse_objects(self, graph):
        result = {}
        for s, p, o in graph.triples((None, rdflib.RDF.type, None)):
            str_o = str(o)
            str_s = str(s)
            try:
                builder = Document.uri_type_map[str_o]
            except KeyError:
                self.logger.info(f'Creating generic object for type {str_o}')
                builder = Identified
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

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read(self, file_path, format='xml'):
        graph = rdflib.Graph()
        with open(file_path, 'r') as infile:
            contents = infile.read()
        graph.parse(data=contents, format=format)
        objects = self._parse_objects(graph)
        self._parse_attributes(objects, graph)
        # Now what?
        # We've got the objects, now we need to store them within the document.
        # Also extract the namespaces from the graph.
