import rdflib

class Ontology:

    def __init__(self, path, ontology_uri):
        self.path = path
        self.graph = rdflib.Graph()
        self.graph.parse(path)
        self.uri = ontology_uri

    def _query(self, sparql, error_msg):
        response = self.graph.query(sparql)
        if not len(response):
            raise LookupError(error_msg)
        return response

    def get_term_by_uri(self, uri):
        query = '''
            SELECT distinct ?label 
            WHERE 
            {{
                <{uri}> rdf:type owl:Class .
                <{uri}> rdfs:label ?label
            }}
            '''.format(uri=uri)
        error_msg = '{} not found'.format(uri)
        response = self._query(query, error_msg)
        term = str([row[0] for row in response][0])
        return term

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
        uri = str([row[0] for row in response][0])
        return uri

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
        uri = str([row[0] for row in response][0])
        return uri

    def query_ontobee(self):

SO = Ontology('ontologies/so.owl', 'http://purl.obolibrary.org/obo/so.owl')
SBO = Ontology('ontologies/SBO_OWL.owl', 'http://biomodels.net/SBO/')
print(SO.get_ontology())
print(SBO.get_ontology())
