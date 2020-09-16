SBOL Extensions
=============================
The Synthetic Biology Open Language is an extensible data representation. This means that users may add new classes to the core data model or add new properties to existing SBOL classes. These are referred to as "extensions" or "custom annotations".  Extension data can be serialized to and parsed from an SBOL file, enabling exchange of the data with other users. This capability is often helpful because applications may produce application-specific data (for example, visual layout information for a visualization tool), or there may be special types of scientific data that the user may want to associate with SBOL data. The extensibility of the SBOL format is another of its advantages compared to traditional bioinformatics formats. This help page provides examples of how to create, access, and exchange extension data.

-----------------------------
Defining Extension Properties
-----------------------------

Extension data may be added or retrieved from an SBOL object using special SBOL property interfaces. Currently the following property interfaces are supported:

.. code:: python

  TextProperty
  URIProperty
  IntProperty
  FloatProperty
  VersionProperty
  DateTimeProperty
  ReferencedObject
  OwnedObject
.. end

Each interface is specialized for a specific data type. For example `TextProperty`, `IntProperty`, and `FloatProperty` contain string, integer, and float values, respectively. The `URIProperty` is used whenever an ontology term is specified. Some properties include special validation rules. For example, the `VersionProperty` will validate whether its string value conforms to `Maven version syntax <https://docs.oracle.com/middleware/1212/core/MAVEN/maven_version.htm#MAVEN8855>`_. Additionally, `DateTimeProperty` will validate whether its string value conforms to `XML Schema Date/Time format <https://www.w3schools.com/xml/schema_dtypes_date.asp>`_. The `OwnedObject` interface is used to define parent-child compositional relationships between objects, while the `ReferencedObject` is used to define associative links between objects.

A property interface can be instantiated by calling its constructor. Property constructors follow a general pattern. The first argument always indicates the object to which the property will be bound. The second argument is always a URI that indicates how the data property will appear when serialized into the contents of an SBOL file. In XML, such a URI is called a "qualified name" or QName. Property constructors also include a cardinality lower and upper bound. Typical values for a lower bound are either 0 (if the field is optional) or 1 (if the field requires a value). Typical upper bound values are either 1 (if the field can contain only a single value) or `math.inf` (if the field can contain an arbitrary length list of values). If desired, a property can also be initialized with a list of validation rules. Validation rules are functions that check whether a property value conforms to a specified rule. They are run every time the value of the property is modified.

Once a property is initialized, it can be assigned and accessed like any other property, as the following example demonstrates. This example associates an x and y coordinate with the ComponentDefinition for layout rendering.

.. code:: python

  doc = sbol2.Document()
  cd = doc.componentDefinitions.create('cd')
  cd.x_coordinate = sbol2.IntProperty(cd, 'http://examples.org#x_coordinate', 0, 1, [])
  cd.y_coordinate = sbol2.IntProperty(cd, 'http://examples.org#y_coordinate', 0, 1, [])
  cd.x_coordinate = 150
  cd.y_coordinate = 100
  print(doc.writeString())
.. end

As you can see, when the file is serialized, the extension data are integrated with core SBOL data:

.. code:: xml

  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:xsd="http://www.w3.org/2001/XMLSchema#" xmlns:sbol="http://sbols.org/v2#" xmlns:ns0="http://examples.org#">
    <sbol:ComponentDefinition rdf:about="http://examples.org/ComponentDefinition/cd/1">
      <ns0:y_coordinate>100</ns0:y_coordinate>
      <sbol:persistentIdentity rdf:resource="http://examples.org/ComponentDefinition/cd"/>
      <ns0:x_coordinate>150</ns0:x_coordinate>
      <sbol:displayId>cd</sbol:displayId>
      <sbol:type rdf:resource="http://www.biopax.org/release/biopax-level3.owl#DnaRegion"/>
      <sbol:version>1</sbol:version>
    </sbol:ComponentDefinition>
  </rdf:RDF>
.. end

By default, extension data are serialized into namespaces with an automatically generated, anonymously prefixed namespace. Thus the extension data are serialized into XML elements as `ns0:x_coordinate` and `ns0:y_coordinate`. Users can specify explicit namespace prefixes by adding namespaces to a `Document` prior to serialization as follows. This has no functional effect but does improve the human readability of the XML.

.. code:: python

  doc.addNamespace('http://examples.org#', 'layout')
  print(doc.writeString())
.. end

Note that the extension data are now serialized under the more descriptive XML tags `layout:x_coordinate` and `layout:y_coordinate`

.. code:: xml

  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:xsd="http://www.w3.org/2001/XMLSchema#" xmlns:layout="http://examples.org#" xmlns:sbol="http://sbols.org/v2#">
    <sbol:ComponentDefinition rdf:about="http://examples.org/ComponentDefinition/cd/1">
      <layout:y_coordinate>100</layout:y_coordinate>
      <sbol:displayId>cd</sbol:displayId>
      <sbol:type rdf:resource="http://www.biopax.org/release/biopax-level3.owl#DnaRegion"/>
      <layout:x_coordinate>150</layout:x_coordinate>
      <sbol:persistentIdentity rdf:resource="http://examples.org/ComponentDefinition/cd"/>
      <sbol:version>1</sbol:version>
    </sbol:ComponentDefinition>
  </rdf:RDF>
.. end

The examples above demonstrate how to write extension data. The following example now demonstrates how to recover extension data upon loading a file. This code block simply takes the output from above and reads it into a new `Document`. Once the `IntProperty` interfaces are initialized, the extension data becomes instantly accessible.

.. code:: xml

  doc2 = sbol2.Document()
  doc2.readString(doc.writeString())
  cd = doc2.componentDefinitions['cd']
  cd.x_coordinate = sbol2.IntProperty(cd, 'http://examples.org#x_coordinate', '0', '1', [])
  cd.y_coordinate = sbol2.IntProperty(cd, 'http://examples.org#y_coordinate', '0', '1', [])
  assert(cd.x_coordinate == 150)
  assert(cd.y_coordinate == 100)
.. end

While in many cases a user knows in advance whether or not a file contains certain types of extension data, it may not always be obvious. Therefore it is possible to inspect the data fields contained in an object using the `getProperties` method. This method lists all the XML QNames associated with an object. Most of the properties listed are core properties, especially those in the `http://sbols.org`, `http://www.w3.org/ns/prov`, and `http://purl.org/dc/terms` namespaces. If any URIs are listed in a namespace that is not one of these, then it is likely custom extension data.

.. code:: python
  print(cd.getProperties)

  ['http://sbols.org/v2#identity', 'http://sbols.org/v2#persistentIdentity', 'http://sbols.org/v2#displayId', 'http://sbols.org/v2#version', 'http://purl.org/dc/terms/title', 'http://purl.org/dc/terms/description', 'http://www.w3.org/ns/prov#wasDerivedFrom', 'http://www.w3.org/ns/prov#wasGeneratedBy', 'http://sbols.org/v2#attachment', 'http://sbols.org/v2#type', 'http://sbols.org/v2#role', 'http://sbols.org/v2#sequence', 'http://examples.org#x_coordinate', 'http://examples.org#y_coordinate', 'http://sbols.org/v2#sequenceAnnotation', 'http://sbols.org/v2#component', 'http://sbols.org/v2#sequenceConstraint']
.. end

-----------------------------------
Extension Classes
-----------------------------------
Extension classes are classes that are derived from SBOL classes. Using extension classes, the data model can be expanded *ad hoc* to represent a wider domain of synthetic biology knowledge. Extension classes allow a user to define an explicit specification for the types of annotation data it contains. This is advantageous when a user wants to efficiently share extension data with other users. A user can share the Python files containing the extension class definition, and other users will have instant access to the extension data.

In the following examples, an extension class includes a class definition containing attributes with SBOL property interfaces, as described in the preceding example. Each class definition must have a builder--a no-argument constructor. The pySBOL parser invokes the builder function when it encounters the RDF type of an object in the SBOL file.

Example 1: Override a Core Class
--------------------------------

The following example illustrates this concept. It defines a `ComponentDefinitionExtension` class which, like the example in the preceding section, includes `x_coordinate` and `y_coordinate` properties. However, in this case, the user does not need to define the property interface, because the extension class definition already does this. The user can simply import the class definition into their code base and access the additional annotation data.

In this example, overriding the core class has the effect that any `ComponentDefinition` that is accessed in a Document after file I/O is now represented as a `ComponentDefinitionExtension` rather than a `ComponentDefinition`. 

.. code:: python

  # Extension class definition
  class ComponentDefinitionOverride(sbol2.ComponentDefinition):

      # Note that a no-argument constructor is defined using a default URI
      def __init__(self, uri='example'):
          super().__init__(uri=uri)
          self.x_coordinate = sbol2.IntProperty(cd, 'http://examples.org#x_coordinate', '0', '1', [])
          self.y_coordinate = sbol2.IntProperty(cd, 'http://examples.org#y_coordinate', '0', '1', [])

  # It is important to register the constructor, so the pySBOL parser can call
  # the correct constructor when it encounters `type_uri` in the SBOL file.
  # The following statement overrides the ComponentDefinition builder so that
  # the ComponentDefinitionExtension builder is invoked by the parser
  Config.register_extension_class(ComponentDefinitionExtension,
                                  sbol2.SBOL_COMPONENT_DEFINITION)

  # Define extension object
  cd = ComponentDefinitionOverride('cd')
  cd.x_coordinate = 150
  cd.y_coordinate = 100

  # Round-trip the extension data
  doc = sbol2.Document()
  doc2 = sbol2.Document()
  doc.add(cd)
  doc2.readString(doc.writeString())

  # Note the object is stored in the Document as a ComponentDefinition
  cd = doc2.componentDefinitions[cd.identity]

  # Confirm the extension data is there
  assert(cd.x_coordinate == 150)
  assert(cd.y_coordinate == 100)

  # Confirm that the specialized type is preserved
  assert(type(cd) is ComponentDefinitionOverride)
.. end

Example 2: Define a New Class
-----------------------------
In the above example, the extension class overrides the core `ComponentDefinition` class, allowing the user to extend the core class definition with extra properties. In other cases, a user may want to extend the SBOL data model with an entirely new class. In this case, the user defines a new class derived from `TopLevel`. The definition of the extension this class differs from the example above in one important respect. It now becomes necessary to specify an RDF type for the new class. The RDF type is a URI represented by the `type_uri` parameter passed to the constructor. The `type_uri` dictates that the object will now be serialized as an entirely new class. The following example defines a custom `Analysis` extension class.

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

Extension classes that do not override a core SBOL class can be accessed from a `Document` through general `add` and `get` methods. 

.. code:: python

  doc = sbol2.Document()
  a = sbol2.Analysis('a')
  doc.add(a)
  also_a = doc.get(a.identity)
  assert(also_a is a)

.. end

Example 3: Composing Extension Objects
--------------------------------------

It is also possible to create extension classes that have a parent-child compositional relationship. In this case the child class should be defined to inherit from `Identified`, while the parent class inherits from `TopLevel`. The child class is referenced through an `OwnedObject` interface. The following example introduces the `DataSheet` class which can now be referenced through the parent `Analysis` class.

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

  doc = sbol2.Document()
  analysis = Analysis('foo')
  doc.add(analysis)
  analysis.dataSheet = DataSheet('foo')
  analysis.dataSheet.transcriptionRate = 96.3
.. end