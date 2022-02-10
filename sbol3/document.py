import collections
import logging
import os
import posixpath
import warnings
from typing import Dict, Callable, List, Optional, Any, Union, Iterable

# import typing for typing.Sequence, which we don't want to confuse
# with sbol3.Sequence
import typing as pytyping

import pyshacl
import rdflib

from . import *
from .object import BUILDER_REGISTER

_default_bindings = {
    'sbol': SBOL3_NS,
    'prov': PROV_NS,
    'om': OM_NS,
    # Should others like SO, SBO, and CHEBI be added?
}


def data_path(path: str) -> str:
    """Expand path based on module installation directory.

    :param path:
    :return:
    """
    # Expand path based on module installation directory
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


class Document:

    @staticmethod
    def register_builder(type_uri: str,
                         builder: Callable[[str, str], Identified]) -> None:
        """A builder function will be called with an identity and a
        keyword argument type_uri.

        builder(identity_uri: str, type_uri: str = None) -> SBOLObject
        """
        Document._uri_type_map[type_uri] = builder

    # Map type URIs to a builder function to construct entities from
    # RDF triples.
    _uri_type_map: Dict[str, Callable[[str, str], Identified]] = BUILDER_REGISTER

    def __init__(self):
        self.logger = logging.getLogger(SBOL_LOGGER_NAME)
        self.objects: List[TopLevel] = []
        # Orphans are non-TopLevel objects that are not otherwise linked
        # into the object hierarchy.
        self.orphans: List[Identified] = []
        self._namespaces: Dict[str, str] = _default_bindings.copy()
        # Non-SBOL triples. These are triples that are not recognized as
        # SBOL. They are stored in _other_rdf for round-tripping purposes.
        self._other_rdf = rdflib.Graph()

    def __str__(self):
        """
        Produce a string representation of the Document.

        :return: A string representation of the Document.
        """
        return self.summary()

    def __len__(self):
        """
        Get the total number of objects in the Document.

        (Returns the same thing as size())

        :return: The total number of objects in the Document.
        """
        return self.size()

    def __contains__(self, item):
        return item in self.objects

    def __iter__(self):
        """Iterate over the top level objects in this document.

        >>> import sbol3
        >>> doc = sbol3.Document()
        >>> doc.read('some_path.ttl')
        >>> for top_level in doc:
        >>>     print(top_level.identity)

        :return: An iterator over the top level objects
        """
        tmp_list = list(self.objects)
        return iter(tmp_list)

    def _build_extension_object(self, identity: str, sbol_type: str,
                                types: List[str]) -> Optional[Identified]:
        custom_types = {
            SBOL_IDENTIFIED: CustomIdentified,
            SBOL_TOP_LEVEL: CustomTopLevel
        }
        if sbol_type not in custom_types:
            msg = f'{identity} has SBOL type {sbol_type} which is not one of'
            msg += f' {custom_types.keys()}. (See Section 6.11)'
            raise SBOLError(msg)
        # Look for a builder associated with one of the rdf:types.
        # If none of the rdf:types have a builder, use the sbol_type's builder
        builder = None
        build_type = None
        for type_uri in types:
            try:
                builder = self._uri_type_map[type_uri]
                build_type = type_uri
                break
            except KeyError:
                logging.warning(f'No builder found for {type_uri}')
        if builder is None:
            builder = custom_types[sbol_type]
            build_type = types[0]
        return builder(identity=identity, type_uri=build_type)

    def _build_object(self, identity: str, types: List[str]) -> Optional[Identified]:
        # Given an identity and a list of RDF types, build an object if possible.
        # If there is 1 SBOL type and we don't know it, raise an exception
        # If there are multiple types and 1 is TopLevel or Identified, then
        #    it is an extension. Use the other types to try to build it. If
        #    no other type is known, build a generic TopLevel or Identified.
        sbol_types = [t for t in types if t.startswith(SBOL3_NS)]
        if len(sbol_types) == 0:
            # If there are no SBOL types in the list. Ignore this entity.
            # Its triples will be stored in self._other_rdf later in the
            # load process.
            return None
        if len(sbol_types) > 1:
            # If there are multiple SBOL types in the list, raise an error.
            # SBOL 3.0.1 Section 5.4: "an object MUST have no more than one
            # rdfType property in the 'http://sbols.org/v3#' namespace"
            msg = f'{identity} has more than one rdfType property in the'
            msg += f' {SBOL3_NS} namespace.'
            raise SBOLError(msg)
        extension_types = {
            SBOL_IDENTIFIED: CustomIdentified,
            SBOL_TOP_LEVEL: CustomTopLevel
        }
        sbol_type = sbol_types[0]
        if sbol_type in extension_types:
            # Build an extension object
            types.remove(sbol_type)
            result = self._build_extension_object(identity, sbol_type, types)
        else:
            try:
                builder = self._uri_type_map[sbol_type]
            except KeyError:
                logging.warning(f'No builder found for {sbol_type}')
                raise SBOLError(f'Unknown type {sbol_type}')
            result = builder(identity=identity, type_uri=sbol_type)
        # Fix https://github.com/SynBioDex/pySBOL3/issues/264
        if isinstance(result, TopLevel):
            # Ensure namespace is not set. It should get set later in the
            # build process. This avoids setting it when the file is invalid
            # and the object has no namespace in the file.
            result.clear_property(SBOL_NAMESPACE)
        # End of fix for https://github.com/SynBioDex/pySBOL3/issues/264
        return result

    def _parse_objects(self, graph: rdflib.Graph) -> Dict[str, SBOLObject]:
        # First extract the identities and their types. Each identity
        # can have either one or two rdf:type properties. If one,
        # create the entity. If two, it is a custom type (see section
        # 6.11 of the spec) and we instantiate it specially.
        #
        identity_types: Dict[str, List[str]] = collections.defaultdict(list)
        for s, p, o in graph.triples((None, rdflib.RDF.type, None)):
            str_o = str(o)
            str_s = str(s)
            identity_types[str_s].append(str_o)
        # Now iterate over the identity->type dict creating the objects.
        result = {}
        for identity, types in identity_types.items():
            obj = self._build_object(identity, types)
            if obj:
                obj.document = self
                result[obj.identity] = obj
        return result

    @staticmethod
    def _parse_attributes(objects, graph):
        for s, p, o in graph.triples((None, None, None)):
            str_s = str(s)
            str_p = str(p)
            try:
                obj = objects[str_s]
            except KeyError:
                # Object is not an SBOL object, skip it
                continue
            if str_p in obj._owned_objects:
                other_identity = str(o)
                other = objects[other_identity]
                obj._owned_objects[str_p].append(other)
            elif str_p == RDF_TYPE:
                # Handle rdf:type specially because the main type(s)
                # will already be in the list from the build_object
                # phase and those entries need to be maintained and
                # we don't want duplicates
                if o not in obj._properties[str_p]:
                    obj._properties[str_p].append(o)
            else:
                obj._properties[str_p].append(o)

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
        self._namespaces = _default_bindings.copy()

    def _parse_graph(self, graph) -> None:
        objects = self._parse_objects(graph)
        self._parse_attributes(objects, graph)
        self._clean_up_singletons(objects)
        # Validate all the objects
        # TODO: Where does this belong? Is this automatic?
        #       Or should a user invoke validate?
        # for obj in objects.values():
        #     obj.validate()
        # Store the TopLevel objects in the Document
        self.objects = [obj for uri, obj in objects.items()
                        if isinstance(obj, TopLevel)]
        # Gather Orphans for future writing.
        # These are expected to be non-TopLevel annotation objects whose owners
        # have no custom implementation (i.e. no builder registered). These objects
        # will be written out as part of Document.write_string()
        self.orphans = []
        for uri, obj in objects.items():
            if obj in self.objects:
                continue
            found = self.find(uri)
            if found:
                continue
            self.orphans.append(obj)
        # Store the namespaces in the Document for later use
        for prefix, uri in graph.namespaces():
            self.bind(prefix, uri)
        # Remove the triples for every object we have loaded, leaving
        # the non-RDF triples for round tripping
        # See https://github.com/SynBioDex/pySBOL3/issues/96
        for uri in objects:
            graph.remove((rdflib.URIRef(uri), None, None))
        # Now tuck away the graph for use in Document.write_string()
        self._other_rdf = graph

    def _guess_format(self, fpath: str):
        rdf_format = rdflib.util.guess_format(fpath)
        if rdf_format == 'nt':
            # Use N-Triples 1.1 format
            # See https://github.com/RDFLib/rdflib/issues/1376
            # See https://github.com/RDFLib/rdflib/issues/1377
            rdf_format = 'nt11'
        return rdf_format

    @staticmethod
    def file_extension(file_format: str) -> str:
        """Return standard extensions when provided the document's file format

        :param file_format: The format of the file
        :return: A file extension, including the leading '.'
        """
        # dictionary having keys as valid file formats,
        # and their standard extensions as value
        types_with_standard_extension = {
            SORTED_NTRIPLES: '.nt',
            NTRIPLES: '.nt',
            JSONLD: '.json',
            RDF_XML: '.xml',
            TURTLE: '.ttl'
        }
        if file_format in types_with_standard_extension:
            return types_with_standard_extension[file_format]
        else:
            raise ValueError('Provided file format is not a valid one.')

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read(self, location: str, file_format: str = None) -> None:
        if file_format is None:
            file_format = self._guess_format(location)
        if file_format is None:
            raise ValueError('Unable to determine file format')
        if file_format == SORTED_NTRIPLES:
            file_format = NTRIPLES
        graph = rdflib.Graph()
        graph.parse(location, format=file_format)
        return self._parse_graph(graph)

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read_string(self, data: str, file_format: str) -> None:
        # TODO: clear the document, this isn't append
        if file_format == SORTED_NTRIPLES:
            file_format = NTRIPLES
        graph = rdflib.Graph()
        graph.parse(data=data, format=file_format)
        return self._parse_graph(graph)

    def _add(self, obj: TopLevel) -> TopLevel:
        """Add objects to the document.
        """
        if not isinstance(obj, TopLevel):
            message = f'Expected TopLevel instance, {type(obj).__name__} found'
            raise TypeError(message)
        found_obj = self.find(obj.identity)
        if found_obj is not None:
            message = f'An entity with identity "{obj.identity}"'
            message += ' already exists in document'
            raise ValueError(message)
        self.objects.append(obj)

        # Assign this document to the object tree rooted
        # in the TopLevel being added
        def assign_document(x: Identified):
            x.document = self
        obj.traverse(assign_document)
        return obj

    def _add_all(self, objects: pytyping.Sequence[TopLevel]) -> pytyping.Sequence[TopLevel]:
        # Perform type check of all objects.
        # We do this to avoid finding out part way through that an
        # object can't be added. That would leave the document in an
        # unknown state.
        for obj in objects:
            if not isinstance(obj, TopLevel):
                if isinstance(obj, Identified):
                    raise TypeError(f'{obj.identity} is not a TopLevel object')
                else:
                    raise TypeError(f'{repr(obj)} is not a TopLevel object')

        # Dispatch to Document._add to add the individual objects
        for obj in objects:
            self._add(obj)
        # return the passed argument
        return objects

    def add(self,
            objects: Union[TopLevel, pytyping.Sequence[TopLevel]]) -> Union[TopLevel, pytyping.Sequence[TopLevel]]:
        # objects must be TopLevel or iterable. If neither, raise a TypeError.
        #
        # Note: Python documentation for collections.abc says "The only
        # reliable way to determine whether an object is iterable is to
        # call iter(obj)." `iter` will raise TypeError if the object is
        # not iterable
        if not isinstance(objects, TopLevel):
            try:
                iter(objects)
            except TypeError:
                raise TypeError('argument must be either TopLevel or Iterable')
        # Now dispatch to the appropriate method
        if isinstance(objects, TopLevel):
            return self._add(objects)
        else:
            return self._add_all(objects)

    def _find_in_objects(self, search_string: str) -> Optional[Identified]:
        # TODO: implement recursive search
        for obj in self.objects:
            # TODO: needs an object.find(search_string) method on ... Identified?
            result = obj.find(search_string)
            if result is not None:
                return result
        return None

    def find(self, search_string: str) -> Optional[Identified]:
        """Find an object by identity URI or by display_id.

        :param search_string: Either an identity URI or a display_id
        :type search_string: str
        :returns: The named object or ``None`` if no object was found

        """
        for obj in self.objects:
            if obj.identity == search_string:
                return obj
            if obj.display_id and obj.display_id == search_string:
                return obj
        return self._find_in_objects(search_string)

    def join_lines(self, lines: List[Union[bytes, str]]) -> Union[bytes, str]:
        """Join lines for either bytes or strings. Joins a list of lines
        together whether they are bytes or strings. Returns a bytes if the input was
        a list of bytes, and a str if the input was a list of str.
        """
        if not lines:
            return ''
        lines_type = type(lines[0])
        if lines_type is bytes:
            # rdflib 5
            return b''.join(lines)
        elif lines_type is str:
            # rdflib 6
            return ''.join(lines)

    def write_string(self, file_format: str) -> str:
        graph = self.graph()
        if file_format == SORTED_NTRIPLES:
            # have RDFlib give us the ntriples as a string
            nt_text = graph.serialize(format=NTRIPLES)
            # split it into lines
            lines = nt_text.splitlines(keepends=True)
            # sort those lines
            lines.sort()
            # write out the lines
            # RDFlib gives us bytes, so open file in binary mode
            result = self.join_lines(lines)
        elif file_format == JSONLD:
            context = {f'@{prefix}': uri for prefix, uri in self._namespaces.items()}
            result = graph.serialize(format=file_format, context=context)
        else:
            result = graph.serialize(format=file_format)
        if type(result) is bytes:
            result = result.decode()
        return result

    def write(self, fpath: str, file_format: str = None) -> None:
        """Write the document to file.

        If file_format is None the desired format is guessed from the
        extension of fpath. If file_format cannot be guessed a ValueError
        is raised.
        """
        if file_format is None:
            file_format = self._guess_format(fpath)
        if file_format is None:
            raise ValueError('Unable to determine file format')
        with open(fpath, 'w') as outfile:
            outfile.write(self.write_string(file_format))

    def graph(self) -> rdflib.Graph:
        """Convert document to an RDF Graph.

        The returned graph is a snapshot of the document and will
        not be updated by subsequent changes to the document.
        """
        graph = rdflib.Graph()
        for prefix, uri in self._namespaces.items():
            graph.bind(prefix, uri)
        for orphan in self.orphans:
            orphan.serialize(graph)
        for obj in self.objects:
            obj.serialize(graph)
        # Add the non-SBOL RDF triples into the generated graph
        graph += self._other_rdf
        return graph

    def bind(self, prefix: str, uri: str) -> None:
        """Bind a prefix to an RDF namespace in the written RDF document.

        These prefixes make the written RDF easier for humans to read.
        These prefixes do not change the semantic meaning of the RDF
        document in any way.
        """
        # Remove any prefix referencing the given URI
        if uri in self._namespaces.values():
            for k, v in list(self._namespaces.items()):
                if v == uri:
                    del self._namespaces[k]
        self._namespaces[prefix] = uri

    def addNamespace(self, namespace: str, prefix: str) -> None:
        """Document.addNamespace is deprecated. Replace with Document.bind.

        Document.addNamespace existed in pySBOL2 and was commonly used.

        Document.addNamespace(namespace, prefix) should now be
        Document.bind(prefix, namespace). Note the change of argument
        order.
        """
        warnings.warn('Use Document.bind() instead', DeprecationWarning)
        self.bind(prefix, namespace)

    def parse_shacl_graph(self, shacl_graph: rdflib.Graph,
                          report: ValidationReport) -> ValidationReport:
        """Convert SHACL violations and warnings into a pySBOL3
        validation report.

        :param shacl_graph: The output graph from pyshacl
        :type shacl_graph: rdflib.Graph
        :param report: The ValidationReport to be populated
        :type report: ValidationReport
        :return: report
        :rtype: ValidationReport
        """
        shacl_ns = rdflib.Namespace('http://www.w3.org/ns/shacl#')
        sh_result_severity = shacl_ns.resultSeverity
        sh_warning = shacl_ns.Warning
        sh_violation = shacl_ns.Violation
        for shacl_report in shacl_graph.subjects(rdflib.RDF.type,
                                                 shacl_ns.ValidationReport):
            for result in shacl_graph.objects(shacl_report, shacl_ns.result):
                object_id = shacl_graph.value(result, shacl_ns.focusNode)
                result_path = shacl_graph.value(result, shacl_ns.resultPath)
                result_message = shacl_graph.value(result, shacl_ns.resultMessage)
                message = f'{result_path}: {result_message}'
                severity = shacl_graph.value(result, sh_result_severity)
                if severity == sh_violation:
                    report.addError(object_id, None, message)
                elif severity == sh_warning:
                    report.addWarning(object_id, None, message)
        return report

    def validate_shacl(self,
                       report: Optional[ValidationReport] = None
                       ) -> ValidationReport:
        """Validate this document using SHACL rules.
        """
        if report is None:
            report = ValidationReport()
        # Save to RDF, then run SHACL over the resulting graph
        data_graph = self.graph()
        shacl_graph = None
        data_graph.parse(data_path(os.path.join('rdf', 'sbol3-shapes.ttl')),
                         format='ttl')
        shacl_report = pyshacl.validate(data_graph=data_graph,
                                        shacl_graph=shacl_graph,
                                        ont_graph=None,
                                        inference=None,
                                        abort_on_first=False,
                                        meta_shacl=False,
                                        advanced=True,
                                        debug=False)
        # Split up the shacl_report tuple
        conforms, results_graph, _ = shacl_report
        if not conforms:
            self.parse_shacl_graph(results_graph, report)
        return report

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        """Validate all objects in this document."""
        if report is None:
            report = ValidationReport()
        for obj in self.objects:
            obj.validate(report)
        self.validate_shacl(report)
        return report

    def find_all(self, predicate: Callable[[Identified], bool]) -> List[Identified]:
        """Executes a predicate on every object in the document tree,
        gathering the list of objects to which the predicate returns true.
        """
        result: List[Identified] = []

        def wrapped_filter(visited: Identified):
            if predicate(visited):
                result.append(visited)
        self.traverse(wrapped_filter)
        return result

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_document` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_document method
        :return: Whatever `visitor.visit_document` returns
        :rtype: Any

        """
        visitor.visit_document(self)

    def traverse(self, func: Callable[[Identified], None]):
        """Enable a traversal of the entire object hierarchy contained
        in this document.
        """
        for obj in self.objects:
            obj.traverse(func)

    def builder(self, type_uri: str) -> Callable[[str, str], Identified]:
        """Lookup up the builder callable for the given type_uri.

        The builder must have been previously registered under this
        type_uri via Document.register_builder().

        :raises: ValueError if the type_uri does not have an associated
                 builder.
        """
        try:
            return self._uri_type_map[type_uri]
        except KeyError:
            raise ValueError(f'No builder for {type_uri}')

    def summary(self):
        """
        Produce a string representation of the Document.
        :return: A string representation of the Document.
        """
        summary = ''
        col_size = 30
        total_core_objects = 0

        type_list = [obj.type_uri for obj in self.objects]
        type_set = list(set(type_list))
        type_set.sort()
        for obj_type in type_set:
            property_name = obj_type[obj_type.rfind('#')+1:]
            obj_count = len([x for x in type_list if x == obj_type])
            total_core_objects += obj_count
            summary += property_name
            summary += '.' * (col_size-len(property_name))
            summary += str(obj_count) + '\n'

        # TODO: Is there a pySBOL equivalent to Annotation Objects?
        # summary += 'Annotation Objects'
        # summary += '.' * (col_size-18)
        # summary += str(self.size() - total_core_objects) + '\n'
        summary += '---\n'
        summary += 'Total: '
        summary += '.' * (col_size-5)
        summary += str(self.size()) + '\n'
        return summary

    def size(self):
        """
        Get the total number of objects in the Document.

        :return: The total number of objects in the Document.
        """
        return len(self.objects)

    def remove(self, objects: Iterable[TopLevel]):
        objects_to_remove = []
        for obj in objects:
            if not isinstance(obj, TopLevel):
                raise ValueError('')
            if obj not in self.objects:
                raise ValueError('')
            objects_to_remove.append(obj)
        # Now do the removal of each top level object and all of its children
        for obj in objects_to_remove:
            obj.remove_from_document()

    def remove_object(self, top_level: TopLevel):
        """Removes the given TopLevel from this document. No referential
        integrity is updated, and the TopLevel object is not informed
        that it has been removed, so it may still have a pointer to this
        document. No errors are raised and no value is returned.

        N.B. You probably want to use `remove` instead of `remove_object`.

        :param top_level: An object to remove
        :return: Nothing
        """
        try:
            self.objects.remove(top_level)
        except ValueError:
            pass

    def migrate(self, top_levels: Iterable[TopLevel]) -> Any:
        """Migrate objects to this document.

        No effort is made to maintain referential integrity. The
        burden of referential integrity lies with the caller of this
        method.

        :param top_levels: The top levels to migrate to this document
        :return: Nothing
        """
        objects = []
        for top_level in top_levels:
            if not isinstance(top_level, TopLevel):
                raise ValueError(f"Object {top_level.identity} is not a TopLevel object")
            objects.append(top_level)
        # Remove each object from its former document if it has one
        for obj in objects:
            obj.remove_from_document()
        # Add each document to this document
        self.add(objects)

    @staticmethod
    def change_object_namespace(top_levels: Iterable[TopLevel],
                                new_namespace: str) -> Any:
        """Change the namespace of all TopLevel objects in `top_levels` to
        new_namespace, regardless of the previous value, while
        maintaining referential integrity among all the top level
        objects in top_levels, including their dependents. The
        namespace change is "in place". No new objects are allocated.

        Note: this operation can result in an invalid Document if the
        change in namespace creates a naming collision. This method
        does not check for this case either before or after the
        operation. It is up to the caller to decide whether this
        operation is safe.

        :param top_levels: objects to change
        :param new_namespace: new namespace for objects
        :return: Nothing
        """
        # Validate the objects and build a map of old name to new name
        objects = []
        identity_map = {}
        for top_level in top_levels:
            if not isinstance(top_level, TopLevel):
                raise ValueError(f'{top_level.identity} is not a TopLevel')
            # if top_level not in self:
            #     raise ValueError(f'{top_level.identity} not in this document')
            # Formulate the new identity
            _, path, display_id = top_level.split_identity()
            new_identity = posixpath.join(new_namespace, path, display_id)
            identity_map[top_level.identity] = top_level
            objects.append((top_level, new_identity))
        # Now change the object identities, and then remap the referenced objects
        for top_level, new_identity in objects:
            top_level.namespace = new_namespace
            top_level.set_identity(new_identity)
            top_level.update_all_dependents(identity_map)
        return None

    def clone(self) -> List[TopLevel]:
        """Clone the top level objects in this document.

        :return: A list of cloned TopLevel objects
        """
        return [tl.clone() for tl in self]

    def copy(self) -> 'Document':
        """Make a copy of this document.

        :return: A new document containing a new set of objects
                 that are identical to the original objects.
        """
        result = Document()
        copy(self, into_document=result)
        return result


def copy(top_levels: Iterable[TopLevel],
         into_namespace: Optional[str] = None,
         into_document: Optional[Document] = None) -> List[TopLevel]:
    """Copy SBOL objects, optionally changing their namespace and
    optionally adding them to a document. Referential integrity among
    the group of provided TopLevel objects is maintained.

    If `new_namespace` is provided, the newly created objects will have
    the provided namespace and will maintain the rest of their
    identities, including the local path and diplay ID.

    If `new_document` is provided, the newly created objects will be
    added to the provided Document.

    :param top_levels: Top Level objects to be copied
    :param into_namespace: A namespace to be given to the new objects
    :param into_document: A document to which the newly created objects
                         will be added
    :return: A list of the newly created objects
    """
    objects = []
    for top_level in top_levels:
        if not isinstance(top_level, TopLevel):
            raise ValueError(f"Object {top_level.identity} is not a TopLevel object")
        objects.append(top_level)
    clones = [tl.clone() for tl in objects]
    if into_namespace is not None:
        Document.change_object_namespace(clones, into_namespace)
    if into_document is not None:
        into_document.add(clones)
    return clones
