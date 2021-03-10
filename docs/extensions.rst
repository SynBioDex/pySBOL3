SBOL Extensions
=============================

The Synthetic Biology Open Language is an extensible data
representation. This means that users may add new classes to the core
data model or add new properties to existing SBOL classes. These are
referred to as "extensions" or "custom annotations".  Extension data
can be serialized to and parsed from an SBOL file, enabling exchange
of the data with other users. This capability is often helpful because
applications may produce application-specific data (for example,
visual layout information for a visualization tool), or there may be
special types of scientific data that the user may want to associate
with SBOL data. The extensibility of the SBOL format is another of its
advantages compared to traditional bioinformatics formats. This help
page provides examples of how to create, access, and exchange
extension data.

-----------------------------
Defining Extension Properties
-----------------------------

Extension data may be added or retrieved from an SBOL object using
special SBOL property interfaces. Currently the following property
interfaces are supported:

.. code:: python

  TextProperty
  URIProperty
  IntProperty
  FloatProperty
  DateTimeProperty
  ReferencedObject
  OwnedObject
.. end

Each interface is specialized for a specific data type. For example
`TextProperty`, `IntProperty`, and `FloatProperty` contain string,
integer, and float values, respectively. The `URIProperty` is used
whenever an ontology term is specified. Some properties include
special validation rules. For example, `DateTimeProperty` will
validate whether its string value conforms to `XML Schema Date/Time
format <https://www.w3schools.com/xml/schema_dtypes_date.asp>`_.
`OwnedObject` is used to define parent-child compositional
relationships between objects, while the `ReferencedObject` is used to
define associative links between objects.

A property can be created by calling a constructor of the same name.
Property constructors follow a general pattern. The first
argument indicates the object to which the property will be
bound. The second argument is a URI that indicates how the data
property will appear when serialized into the contents of an SBOL
file. In XML, such a URI is called a "qualified name" or
QName. Property constructors also include a cardinality lower and
upper bound. Typical values for a lower bound are either 0 (if the
field is optional) or 1 (if the field requires a value). Typical upper
bound values are either 1 (if the field can contain only a single
value) or `math.inf` (if the field can contain an arbitrary length
list of values).

Once a property is initialized, it can be assigned and accessed like
any other property, as the following example demonstrates. This
example associates an x and y coordinate with the Component
for layout rendering.

.. code:: python

    >>> import sbol3
    RDFLib Version: 5.0.0
    >>> c1 = sbol3.Component('http://example.org/sbol3/c1', sbol3.SBO_DNA)
    >>> c1.x_coordinate = sbol3.IntProperty(c1, 'http://example.org/my_vis#x_coordinate', 0, 1)
    >>> c1.y_coordinate = sbol3.IntProperty(c1, 'http://example.org/my_vis#y_coordinate', 0, 1)
    >>> c1.x_coordinate = 150
    >>> c1.y_coordinate = 175
    >>> doc = sbol3.Document()
    >>> doc.add(c1)
    >>> print(doc.write_string(sbol3.SORTED_NTRIPLES).decode())

    <http://example.org/sbol3/c1> <http://example.org/my_vis#x_coordinate> "150"^^<http://www.w3.org/2001/XMLSchema#integer> .
    <http://example.org/sbol3/c1> <http://example.org/my_vis#y_coordinate> "175"^^<http://www.w3.org/2001/XMLSchema#integer> .
    <http://example.org/sbol3/c1> <http://sbols.org/v3#displayId> "c1" .
    <http://example.org/sbol3/c1> <http://sbols.org/v3#type> <https://identifiers.org/SBO:0000251> .
    <http://example.org/sbol3/c1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v3#Component> .
    
    >>> 

.. end

As you can see, when the file is serialized, the extension data are integrated with core SBOL data.

The example above demonstrates how to write extension data. The
following example demonstrates how to recover extension data upon
loading a file. This code block simply takes the output from above and
reads it into a new `Document`. Once the `IntProperty` interfaces are
initialized, the extension data becomes accessible.

.. code:: xml

    >>> doc2 = sbol3.Document()
    >>> doc2.read_string(doc.write_string(sbol3.NTRIPLES), sbol3.NTRIPLES)
    >>> c1a = doc2.find('http://example.org/sbol3/c1')
    >>> c1a.display_id
    'c1'

    # See that x_coordinate is not known
    >>> c1a.x_coordinate
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/path/to/sbol3/object.py", line 35, in __getattribute__
        result = object.__getattribute__(self, name)
    AttributeError: 'Component' object has no attribute 'x_coordinate'
    
    # Now define the extension properties
    >>> c1a.x_coordinate = sbol3.IntProperty(c1, 'http://example.org/my_vis#x_coordinate', 0, 1)
    >>> c1a.y_coordinate = sbol3.IntProperty(c1, 'http://example.org/my_vis#y_coordinate', 0, 1)
    >>> c1a.x_coordinate
    150
    >>> c1a.y_coordinate
    175

.. end

While in many cases a user knows in advance whether or not a file
contains certain types of extension data, it may not always be
obvious. Therefore it is possible to inspect the data fields contained
in an object using the `properties` attribute. This attribute contains
the URIs of the properties associated with an object. Most of the
properties listed will be core properties, especially those in the
`http://sbols.org`, `http://www.w3.org/ns/prov`, and
`http://purl.org/dc/terms` namespaces. If any URIs are listed in a
namespace that is not one of these, then it is likely custom extension
data.

.. code:: python

    >>> import pprint
    >>> pprint.pprint(sorted(c1a.properties))
    ['http://example.org/my_vis#x_coordinate',
     'http://example.org/my_vis#y_coordinate',
     'http://sbols.org/v3#description',
     'http://sbols.org/v3#displayId',
     'http://sbols.org/v3#hasAttachment',
     'http://sbols.org/v3#hasModel',
     'http://sbols.org/v3#hasSequence',
     'http://sbols.org/v3#name',
     'http://sbols.org/v3#role',
     'http://sbols.org/v3#type',
     'http://www.w3.org/ns/prov#wasDerivedFrom',
     'http://www.w3.org/ns/prov#wasGeneratedBy']

.. end

-----------------------------------
Extension Classes
-----------------------------------

Extension classes are classes that are derived from SBOL
classes. Using extension classes, the data model can be expanded *ad
hoc* to represent a wider domain of synthetic biology
knowledge. Extension classes allow a user to define an explicit
specification for the types of annotation data it contains. This is
advantageous when a user wants to efficiently share extension data
with other users. A user can share the Python files containing the
extension class definition, and other users will have instant access
to the extension data.

In the following examples, an extension class includes a class
definition containing attributes with SBOL property interfaces, as
described in the preceding example. Each class definition must have a
builder function. The pySBOL parser invokes the builder function when
it encounters the RDF type of an object in the SBOL file.

Example 1: Override a Core Class
--------------------------------

The following example illustrates this concept. It defines a
`ComponentExtension` class which, like the example in the
preceding section, includes `x_coordinate` and `y_coordinate`
properties. However, in this case, the user does not need to define
the property interface, because the extension class definition already
does this. The user can simply import the class definition into their
code base and access the additional annotation data.

In this example, overriding the core class has the effect that any
`Component` that is accessed in a Document after file I/O is now
represented as a `ComponentExtension` rather than a `Component`.

.. literalinclude:: ../examples/compext.py
  :language: python
  :caption: examples/compext.py

In a Python interpreter with the `ComponentExtension` class loaded you
can now use the `x_coordinate` and `y_coordinate` properties
automatically. Here is an example that creates a `ComponentExtension`,
sets the new properties, then saves it to file. The saved file is then
loaded and the new properties are preserved.

.. code:: python

    >>> c = ComponentExtension('http://example.org/sbol3/c1', sbol3.SBO_DNA)
    >>> c.x_coordinate
    0
    >>> c.y_coordinate
    0
    >>> c.x_coordinate = 150
    >>> c.y_coordinate = 100
    >>>
    >>> # Round trip the document
    >>> doc = sbol3.Document()
    >>> doc.add(c)
    >>> doc2 = sbol3.Document()
    >>> doc2.read_string(doc.write_string(sbol3.NTRIPLES), sbol3.NTRIPLES)
    >>>
    >>> # Fetch the Component out of the new document
    >>> c2 = doc2.find('c1')
    >>> c2.x_coordinate
    150
    >>> c2.y_coordinate
    100
    >>> type(c2).__name__
    'ComponentExtension'

.. end


Example 2: Define a New Class
-----------------------------

In the above example, the extension class overrides the core
`ComponentDefinition` class, allowing the user to extend the core
class definition with extra properties. In other cases, a user may
want to extend the SBOL data model with an entirely new class. In this
case, the user defines a new class derived from `TopLevel`. The
definition of this extension class differs from the example above in
one important respect. It now becomes necessary to specify an RDF type
for the new class. The RDF type is a URI represented by the `type_uri`
parameter passed to the constructor. The `type_uri` dictates that the
object will now be serialized as an entirely new class. The following
example defines a custom `Analysis` extension class.

.. literalinclude:: ../examples/analysisext.py
  :language: python
  :caption: examples/analysisext.py

.. code:: python

  class Analysis(sbol2.TopLevel):

      RDF_TYPE = 'http://examples.org#Analysis'

      def __init__(self, uri=None, model=None):
          # Override the default type_uri that is used when serializing
          super().__init__(uri=uri,
                           type_uri=Analysis.RDF_TYPE)
          self.fittedModel = sbol2.ReferencedObject(self, 'http://examples.org#fit',
                                                    sbol2.SBOL_MODEL, 0, 1, [])

  # Register the constructor with the parser
  Config.register_extension_class(Analysis, Analysis.RDF_TYPE)
.. end

Extension classes that do not override a core SBOL class can be
accessed from a `Document` through general `add` and `find` methods.

.. code:: python

    >>> doc = sbol3.Document()
    >>> a = Analysis('http://example.org/sbol3/a1')
    >>> doc.add(a)
    >>> also_a = doc.find(a.identity)
    >>> also_a is a
    True

.. end


Example 3: Composing Extension Objects
--------------------------------------

It is also possible to create extension classes that have a
parent-child compositional relationship. In this case the child class
should be defined to inherit from `CustomIdentified`, while the parent
class inherits from `CustomTopLevel`. The child class is referenced
through an `OwnedObject` interface. The following example introduces
the `DataSheet` class which can now be referenced through the parent
`Analysis` class.

.. literalinclude:: ../examples/datasheetext.py
  :language: python
  :caption: examples/datasheetext.py


.. code:: python

  class DataSheet(sbol2.Identified):

      RDF_TYPE = 'http://examples.org#DataSheet'

      def __init__(self, uri='example'):
          super().__init__(uri=uri,
                           type_uri=DataSheet.RDF_TYPE)
          self.transcriptionRate = sbol2.FloatProperty(self, 'http://examples.org#txRate',
                                                       0, 1, [])

  class Analysis(sbol2.TopLevel):

      RDF_TYPE = 'http://examples.org#Analysis'

      def __init__(self, uri=None, model=None):
          super().__init__(uri=uri,
                           type_uri=Analysis.RDF_TYPE)
          self.fittedModel = sbol2.ReferencedObject(self, 'http://examples.org#fittedModel',
                                                    sbol2.SBOL_MODEL, 0, 1, [])
          self.dataSheet = sbol2.OwnedObject(self, 'http://examples.org#dataSheet',
                                             DataSheet, 0, 1, [])

  # Register the constructors with the parser
  Config.register_extension_class(Analysis, Analysis.RDF_TYPE)
  Config.register_extension_class(DataSheet, DataSheet.RDF_TYPE)

.. end

.. code:: python

    >>> doc = sbol3.Document()
    >>> a = Analysis('http://example.org/sbol3/a1')
    >>> doc.add(a)
    >>> a.data_sheet = DataSheet()
    >>> a.data_sheet.transcription_rate = 96.3
    >>> a.data_sheet.transcription_rate
    96.3

.. end
