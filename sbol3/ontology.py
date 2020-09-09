import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib

class Ontology():

    endpoint = SPARQLWrapper('http://sparql.hegroup.org/sparql/')
    endpoint.setReturnFormat(JSON)

    def __init__(self, path, ontology_uri):
        self.path = path
        self.graph = rdflib.Graph()
        self.uri = ontology_uri        

    def _query(self, sparql, error_msg):
        '''
        This is a generalized back-end for querying ontologies. By default it performs
        SPARQL queries through a network endpoint, because loading an ontology from a
        local graph takes a while and uses up memory.  However, once a graph is loaded
        locally, subsequent queries will be performed directly on the graph.
        '''
        if len(self.graph):
            # If the ontology graph has been loaded locally, query that rather
            # than querying over the network
            response = self.graph.query(sparql)
            response = Ontology._convert_rdflib_response(response)
        else:
            try:
                # If no ontology graph is located, query the network endpoint
                Ontology.endpoint.setQuery(sparql)
                response = Ontology.endpoint.query()
                response = Ontology._convert_ontobee_response(response)
            except urllib.error.URLError:
                # If the connection fails, load the ontology locally
                self.graph.parse(self.path)
                response = self.graph.query(sparql)
                response = Ontology._convert_rdflib_response(response)
        if not len(response):
            raise LookupError(error_msg)
        return response  

    def _convert_ontobee_response(response):
        '''
        Ontobee SPARQL interface returns JSON. This extracts and flattens the queried
        variables into a list
        '''
        response = response.convert()  # Convert http response to JSON
        converted_response = []
        for var, binding in zip(response['head']['vars'], response['results']['bindings']):
            converted_response.append(binding[var]['value'])
        return converted_response

    def _convert_rdflib_response(response):
        '''
        Extracts and flattens queried variables from rdflib response into a list
        '''
        return [str(row[0]) for row in response]

    def get_term_by_uri(self, uri):
        '''
        '''
        query = '''
            SELECT distinct ?label
            WHERE 
            {{
                <{uri}> rdf:type owl:Class .
                <{uri}> rdfs:label ?label .
            }}
            '''.format(uri=uri)
        error_msg = '{} not found'.format(uri)
        response = self._query(query, error_msg)
        return response[0]

    def get_uri_by_term(self, term):
        # queries to the sequence ontology require the xsd:string datatype
        # whereas queries to the systems biology ontology do not
        query = '''
            SELECT distinct ?uri 
            WHERE 
            {{
                ?uri rdf:type owl:Class .
                {{?uri rdfs:label "{term}"^^xsd:string}} UNION
                {{?uri rdfs:label "{term}"}}
            }}
            '''.format(term=term)
        error_msg = '{} not found'.format(term)
        response = self._query(query, error_msg)
        return response[0]

    def get_ontology(self):
        query = '''
            SELECT distinct ?ontology_uri 
            WHERE 
              {
                ?ontology_uri a owl:Ontology
              }
            '''
        error_msg = 'Graph not found'
        response = self._query(query, error_msg)
        return response[0]

    def __getattr__(self, name):     
        if name in self.__getattribute__('__dict__'):
            return self.__getattribute__(name)
        else:
            return self.__getattribute__('get_uri_by_term')(name)

SO = Ontology('ontologies/so.owl', 'http://purl.obolibrary.org/obo/so.owl')
SBO = Ontology('ontologies/SBO_OWL.owl', 'http://biomodels.net/SBO/')
