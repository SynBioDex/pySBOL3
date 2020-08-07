# --------------------------------------------------
# Constants to support SBOL 3
# See https://sbolstandard.org/wp-content/uploads/2020/04/SBOL3.0specification.pdf
# --------------------------------------------------

SBOL_LOGGER_NAME = 'sbol3'

# ----------
# Namespaces
# ----------

SBOL3_NS = 'http://sbols.org/v3#'
SBOL2_NS = 'http://sbols.org/v2#'
SBOL1_NS = 'http://sbols.org/v1#'

CHEBI_NS = 'http://identifiers.org/chebi/CHEBI:'

# Namespace for Sequence Ontology (SO) terms
SO_NS = "http://identifiers.org/so/SO:"

# Provenance
PROV_NS = 'https://www.w3.org/TR/prov-o/'

# ----------
# SBOL 3 terms
# ----------
SBOL_DESCRIPTION = SBOL3_NS + 'description'
SBOL_DISPLAY_ID = SBOL3_NS + 'displayId'
SBOL_ELEMENTS = SBOL3_NS + 'elements'
SBOL_ENCODING = SBOL3_NS + 'encoding'
SBOL_FRAMEWORK = SBOL3_NS + 'framework'
SBOL_HAS_ATTACHMENT = SBOL3_NS + 'hasAttachment'
SBOL_LANGUAGE = SBOL3_NS + 'language'
SBOL_MODELS = SBOL3_NS + 'hasModel'
SBOL_NAME = SBOL3_NS + 'name'
SBOL_ROLE = SBOL3_NS + 'role'
SBOL_SOURCE = SBOL3_NS + 'source'
SBOL_SEQUENCES = SBOL3_NS + 'hasSequence'
SBOL_TYPE = SBOL3_NS + 'type'


# ----------
# Provenance terms
# ----------
PROV_DERIVED_FROM = PROV_NS + 'wasDerivedFrom'
PROV_GENERATED_BY = PROV_NS + 'wasGeneratedBy'


# ----------
# Component roles
#
# * These are common, others can be used as well.
# * See the SBOL 3 spec, Section 6.4, Table 4
# ----------
SO_PROMOTER = SO_NS + "0000167"
SO_RBS = SO_NS + "0000139"
SO_CDS = SO_NS + "0000316"
SO_TERMINATOR = SO_NS + "0000141"
SO_GENE = SO_NS + "0000704"
SO_OPERATOR = SO_NS + "0000057"
SO_ENGINEERED_GENE = SO_NS + "0000280"
SO_MRNA = SO_NS + "0000234"
CHEBI_EFFECTOR = CHEBI_NS + '35224'
SO_TRANSCRIPTION_FACTOR = SO_NS + "0003700"
