Computer-aided Design for Synthetic Biology
===========================================

See `Full Example Code <#id1>`_ for full example code.

---------------------------------
Design Abstraction
---------------------------------

An advantage of the SBOL data format over GenBank is the ability to represent DNA as abstract components without specifying an exact sequence. An **abstract design** can be used as a template, with sequence information filled in later. In SBOL, a ComponentDefinition represents a biological component whose general function is known while its sequence is currently either unknown or unspecified. The intended function of the component is specified using a descriptive term from the Sequence Ontology (SO), a standard vocabulary for describing genetic parts. As the following example shows, some common SO terms are built in to PySBOL2 as pre-defined constants (see `constants.py <https://github.com/SynBioDex/pySBOL2/blob/master/sbol2/constants.py>`_). This code example defines the new component as a gene by setting its `roles` property to the SO term for `gene`.  Other terms may be found by browsing the `Sequence Ontology <http://www.sequenceontology.org/browser/obob.cgi>`_ online.

.. code:: python

    # Construct an abstract design for a gene
    gene = ComponentDefinition('gene_example')
    gene.roles = SO_GENE

.. end

**Design abstraction** is an important engineering principle for synthetic biology. Abstraction enables the engineer to think at a high-level about functional characteristics of a system while hiding low-level physical details. For example, in electronics, abstract schematics are used to describe the function of a circuit, while hiding the physical details of how a printed circuit board is laid out. Computer-aided design (CAD) programs allow the engineer to easily switch back and forth between abstract and physical representations of a circuit. In the same spirit, PySBOL2 enables a CAD approach for designing genetic constructs and other forms of synthetic biology.

-------------------------------
Hierarchical DNA Assembly
-------------------------------

PySBOL2 also includes methods for assembling biological components (also referred to as biological parts in the synthetic biology literature) into **abstraction hierarchies**. Abstraction hierarchies are important from an engineering perspective because they allow engineers to assemble complicated systems from more basic components. Abstraction hierarchies are also important from a biological perspective, because DNA sequences and biological structures in general exhibit hierarchical organization, from the genome, to operons, to genes, to lower level genetic operators. The following code assembles an abstraction hierarchy that describes a gene cassette. Note that subcomponents must belong to a `Document` in order to be assembled, so a `Document` is passed as a parameter.

The gene cassette below is composed of genetic subcomponents including a promoter, ribosome binding site (RBS), coding sequence (CDS), and transcriptional terminator, expressed in SBOL Visual schematic glyphs. The next example demonstrates how an abstract design for this gene is assembled from its subcomponents.

.. code:: python

    gene.assemblePrimaryStructure([ r0010, b0032, e0040, b0012 ], doc)
.. end

After creating an abstraction hierarchy, it is then possible to iterate through an object's primary structure of components:

.. code:: python

    for component_definition in gene.getPrimaryStructure()):
        print (component_definition.identity)
.. end

This returns a list of `ComponentDefinitions` arranged in their primary sequence. Occasionally it is also helpful to get `Components` arranged in their primary sequence as well. Note that the example below produces the same output as the example above, and may be helpful for understanding the relationship between `Components` and `ComponentDefinitions`.

.. code:: python

    for component in gene.getPrimaryStructureComponents():
        print (component.definition)
.. end

 *Caution!* It is also possible to iterate through components as follows, but this way is *not* guaranteed to return `Components` in order of primary sequence. This is because member `Components` in an abstraction hierarchy are not always guaranteed to be composed into a primary sequence.

.. code:: python

    for component in gene.components:
        print (component.definition)
.. end

----------------------------
Editing a Primary Structure
----------------------------

Given an abstract representation of a primary structure as above, it is possible to modify it by inserting and deleting `Components`. The following example deletes the R0010 promoter and replaces it with the R0011 promoter

.. code:: python

    primary_structure = gene.getPrimaryStructureComponents()
    b0032_component = primary_structure[1]
    gene.deleteUpstreamComponent(b0032_component) 

    r0011 = ComponentDefinition('r0011')
    r0011.roles = SO_CDS
    gene.insertUpstreamComponent(b0032_component, r0011)
.. end

-------------------------------
Sequence Assembly
-------------------------------

A **complete design** adds explicit sequence information to the components in a **template design** or **abstraction hierarchy**. In order to complete a design, `Sequence` objects must first be created and associated with the promoter, CDS, RBS, terminator subcomponents. In contrast to the `ComponentDefinition.assemble() <autoapi/sbol2/componentdefinition/index.html#sbol2.componentdefinition.ComponentDefinition.assemble>`_ method, which assembles a template design, the `ComponentDefinition.compile` method recursively generates the complete sequence of a hierarchical design from the sequence of its subcomponents. Compiling a DNA sequence is analogous to a programmer compiling their code. In order to `compile` a `ComponentDefinition`, you must first assemble a template design from `ComponentDefinitions`, as described in the previous section.

.. code:: python 

    target_sequence = gene.compile()
.. end

The `compile` method returns the target sequence as a string. In addition, it creates a new `Sequence` object and assigns the target sequence to its `elements` property
 
--------------------------------------------------------------
Genome Integration
--------------------------------------------------------------
In some cases, it may be useful to represent integration of vectors / transposons into genomes. The `integrateAtBaseCoordinate` method supports integration operations and produces a parsimonious representation of primary structure that is useful for manipulating large constructs. The following example demonstrates integration of the `gene` construct from the examples above into a `wild_type_genome`, thus generating the `integrated_genome`.

.. code:: python

    integrated_genome = ComponentDefinition('integrated_genome')
    integrated_genome.sequence = Sequence('integrated_genome_sequence')
    wild_type_genome = ComponentDefinition('wild_type_genome')
    wild_type_genome.sequence = Sequence('wild_type_genome_sequence')
    wild_type_genome.sequence.elements = 'gggggggggg'
    integrated_genome.integrateAtBaseCoordinate(wild_type_genome, gene, 5)
    integrated_genome.compile()  # Calculate sequence of the integrated genome

.. end
    
-------------------------------
Full Example Code
-------------------------------

Full example code is provided below, which will create a file called "gene_cassette.xml".
This example is available as
`examples/gene_cassette.py <https://github.com/SynBioDex/pySBOL2/blob/master/examples/gene_cassette.py>`_
in the pySBOL2 source code.

.. code:: python

    from sbol2 import *

    setHomespace('http://sys-bio.org')
    doc = Document()

    gene = ComponentDefinition('gene_example')
    r0010 = ComponentDefinition('R0010')
    b0032 = ComponentDefinition('B0032')
    e0040 = ComponentDefinition('E0040')
    b0012 = ComponentDefinition('B0012')

    r0010.roles = SO_PROMOTER
    b0032.roles = SO_CDS
    e0040.roles = SO_RBS
    b0012.roles = SO_TERMINATOR

    doc.addComponentDefinition(gene)
    doc.addComponentDefinition([r0010, b0032, e0040, b0012])

    gene.assemblePrimaryStructure([r0010, b0032, e0040, b0012])

    first = gene.getFirstComponent()
    print(first.identity)
    last = gene.getLastComponent()
    print(last.identity)

    r0010.sequence = Sequence('R0010', 'ggctgca')
    b0032.sequence = Sequence('B0032', 'aattatataaa')
    e0040.sequence = Sequence('E0040', "atgtaa")
    b0012.sequence = Sequence('B0012', 'attcga')

    target_sequence = gene.compile()
    print(gene.sequence.elements)

    result = doc.write('gene_cassette.xml')
    print(result)

.. end
