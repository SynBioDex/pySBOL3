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
SBOL_CARDINALITY = SBOL3_NS + 'cardinality'
SBOL_COMPONENT = SBOL3_NS + 'Component'
SBOL_CONSTRAINT = SBOL3_NS + 'Constraint'
SBOL_CONSTRAINTS = SBOL3_NS + 'hasConstraint'
SBOL_CUT = SBOL3_NS + 'Cut'
SBOL_DESCRIPTION = SBOL3_NS + 'description'
SBOL_DISPLAY_ID = SBOL3_NS + 'displayId'
SBOL_ELEMENTS = SBOL3_NS + 'elements'
SBOL_ENCODING = SBOL3_NS + 'encoding'
SBOL_END = SBOL3_NS + 'end'
SBOL_ENTIRE_SEQUENCE = SBOL3_NS + 'EntireSequence'
SBOL_FEATURES = SBOL3_NS + 'hasFeature'
SBOL_FRAMEWORK = SBOL3_NS + 'framework'
SBOL_HAS_ATTACHMENT = SBOL3_NS + 'hasAttachment'
SBOL_INSTANCE_OF = SBOL3_NS + 'instanceOf'
SBOL_LANGUAGE = SBOL3_NS + 'language'
SBOL_LOCATION = SBOL3_NS + 'hasLocation'
SBOL_MODEL = SBOL3_NS + 'Model'
SBOL_MODELS = SBOL3_NS + 'hasModel'
SBOL_NAME = SBOL3_NS + 'name'
SBOL_OBJECT = SBOL3_NS + 'object'
SBOL_ORDER = SBOL3_NS + 'order'
SBOL_ORIENTATION = SBOL3_NS + 'orientation'
SBOL_RANGE = SBOL3_NS + 'Range'
SBOL_RESTRICTION = SBOL3_NS + 'restriction'
SBOL_ROLE = SBOL3_NS + 'role'
SBOL_SEQUENCE = SBOL3_NS + 'Sequence'
SBOL_SOURCE = SBOL3_NS + 'source'
SBOL_SEQUENCES = SBOL3_NS + 'hasSequence'
SBOL_SOURCE_LOCATION = SBOL3_NS + 'sourceLocation'
SBOL_START = SBOL3_NS + 'start'
SBOL_SUBCOMPONENT = SBOL3_NS + 'SubComponent'
SBOL_SUBJECT = SBOL3_NS + 'subject'
SBOL_TYPE = SBOL3_NS + 'type'
SBOL_VARIABLE = SBOL3_NS + 'variable'
SBOL_VARIABLE_COMPONENT = SBOL3_NS + 'VariableComponent'
SBOL_VARIANT = SBOL3_NS + 'variant'
SBOL_VARIANT_COLLECTION = SBOL3_NS + 'variantCollection'
SBOL_VARIANT_DERIVATION = SBOL3_NS + 'variantDerivation'

# Valid values for Variable Component cardinality
# See SBOL3 Section 6.5 Table 13
SBOL_ONE = SBOL3_NS + 'one'
SBOL_ONE_OR_MORE = SBOL3_NS + 'oneOrMore'
SBOL_ZERO_OR_MORE = SBOL3_NS + 'zeroOrMore'
SBOL_ZERO_OR_ONE = SBOL3_NS + 'zeroOrOne'

PYSBOL3_MISSING = 'https://github.com/synbiodex/pysbol3#missing'


# ----------
# Provenance terms
# ----------
PROV_DERIVED_FROM = PROV_NS + 'wasDerivedFrom'
PROV_GENERATED_BY = PROV_NS + 'wasGeneratedBy'


# ----------
# Component/Feature roles
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

# ----------
# Feature orientations
#
# * See the SBOL 3 spec, Section 6.4.1, Table 5
# ----------
SBOL_INLINE = SBOL3_NS + 'inline'
SBOL_REVERSE_COMPLEMENT = SBOL3_NS + 'reverseComplement'
