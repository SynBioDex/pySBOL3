import rdflib

# ----------
# Namespaces
# ----------

SBOL3_NS = 'http://sbols.org/v3#'
SBOL2_NS = 'http://sbols.org/v2#'
SBOL1_NS = 'http://sbols.org/v1#'

CHEBI_NS = 'http://identifiers.org/chebi/CHEBI:'
# Namespace for Sequence Ontology (SO) terms
SO_NS = "http://identifiers.org/so/SO:"

PROV_NS = rdflib.Namespace('https://www.w3.org/TR/prov-o/')

# ----------
# SBOL 3 terms
# ----------
SBOL_DESCRIPTION = SBOL3_NS + 'description'
SBOL_DISPLAY_ID = SBOL3_NS + 'displayId'
SBOL_FRAMEWORK = SBOL3_NS + 'framework'
SBOL_HAS_ATTACHMENT = SBOL3_NS + 'hasAttachment'
SBOL_LANGUAGE = SBOL3_NS + 'language'
SBOL_MODELS = SBOL3_NS + 'hasModel'
SBOL_NAME = SBOL3_NS + 'name'
SBOL_ROLE = SBOL3_NS + 'role'
SBOL_SOURCE = SBOL3_NS + 'source'
SBOL_SEQUENCES = SBOL3_NS + 'hasSequence'
SBOL_TYPE = SBOL3_NS + 'type'

# An SO term and possible value for Component.role attribute
SO_PROMOTER = SO_NS + "0000167"
# An SO term and possible value for Component.role attribute
SO_RBS = SO_NS + "0000139"
# An SO term and possible value for Component.role attribute
SO_CDS = SO_NS + "0000316"
# An SO term and possible value for Component.role attribute
SO_TERMINATOR = SO_NS + "0000141"
# An SO term and possible value for Component.role attribute
SO_GENE = SO_NS + "0000704"
# An SO term and possible value for Component.role attribute
SO_OPERATOR = SO_NS + "0000057"
# An SO term and possible value for Component.role attribute
SO_ENGINEERED_GENE = SO_NS + "0000280"
# An SO term and possible value for Component.role attribute
SO_MRNA = SO_NS + "0000234"
# An SO term and possible value for Component.role attribute
CHEBI_EFFECTOR = CHEBI_NS + '35224'
# An SO term and possible value for Component.role attribute
SO_TRANSCRIPTION_FACTOR = SO_NS + "0003700"
