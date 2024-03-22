============================
SBOL v3 Data Model in Action
============================

Introduction
============

This documentation is based on a Jupyter Notebook tutorial presented at IWBDA 2023, demonstrating the SBOL v3 data model.

`IWBDA 2023 SBOL 3 Tutorial Slides <https://github.com/SynBioDex/Community-Media/blob/master/2023/IWBDA23/SBOL3-IWBDA-2023.pptx>`_

`Jupyter Notebook <https://github.com/SynBioDex/SBOL-Notebooks/blob/main/iwbda_2023_examples.ipynb>`_

Installation
=============

Sbol Utilities is a Python package that provides a set of utility functions for working with the SBOL3 data model. 
It is available on PyPI and can be installed using pip.

.. code-block:: bash

    pip install sbol_utilities

This will also install `pySBOL3` and `tyto`, which are dependencies of `sbol_utilities`.

Using the SBOLv3 Data Model
===========================

Import the necessary modules from the `sbol3` and `sbol_utilities` packages.

.. code-block:: python

    from sbol3 import *
    from sbol_utilities.calculate_sequences import compute_sequence
    from sbol_utilities.component import *
    from sbol_utilities.helper_functions import url_to_identity
    import tyto

We will use `igem` suffix as the default namespace for the examples in this tutorial.

.. code-block:: python

    set_namespace('https://synbiohub.org/public/igem/')
    doc = Document()

GFP Expression Cassette
=======================

Construct a simple part and add it to the Document.

.. code-block:: python

    i13504 = Component('i13504', SBO_DNA)
    i13504.name = 'iGEM 2016 interlab reporter'
    i13504.description = 'GFP expression cassette used for 2016 iGEM interlab study'
    i13504.roles.append(tyto.SO.engineered_region)

Add the GFP expression cassette to the document. Notice that the object added is also returned, so this can be used as a pass-through call.

.. code-block:: python

    doc.add(i13504)

Expression Cassette parts
==========================

Here we will create a part-subpart hierarchy. We will also start using `SBOL-Utilities <https://github.com/synbiodex/sbol-utilities>` _ to make it easier to create parts and to assemble those parts into a hierarchy.
First, create the RBS component...

.. code-block:: python

    b0034, b0034_seq = doc.add(rbs('B0034', sequence='aaagaggagaaa', name='RBS (Elowitz 1999)'))

Next, create the GFP component

.. code-block:: python

    e0040_sequence = 'atgcgtaaaggagaagaacttttcactggagttgtcccaattcttgttgaattagatggtgatgttaatgggcacaaattttctgtcagtggagagggtgaaggtgatgcaacatacggaaaacttacccttaaatttatttgcactactggaaaactacctgttccatggccaacacttgtcactactttcggttatggtgttcaatgctttgcgagatacccagatcatatgaaacagcatgactttttcaagagtgccatgcccgaaggttatgtacaggaaagaactatatttttcaaagatgacgggaactacaagacacgtgctgaagtcaagtttgaaggtgatacccttgttaatagaatcgagttaaaaggtattgattttaaagaagatggaaacattcttggacacaaattggaatacaactataactcacacaatgtatacatcatggcagacaaacaaaagaatggaatcaaagttaacttcaaaattagacacaacattgaagatggaagcgttcaactagcagaccattatcaacaaaatactccaattggcgatggccctgtccttttaccagacaaccattacctgtccacacaatctgccctttcgaaagatcccaacgaaaagagagaccacatggtccttcttgagtttgtaacagctgctgggattacacatggcatggatgaactatacaaataataa'
    e0040, _ = doc.add(cds('E0040', sequence=e0040_sequence, name='GFP'))

Finally, create the terminator component

.. code-block:: python

    b0015_sequence = 'ccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata'
    b0015, _ = doc.add(terminator('B0015', sequence=b0015_sequence, name='double terminator'))

Now construct the part-subpart hierarchy and order the parts: RBS before CDS, CDS before terminator

.. code-block:: python

    order(b0034, e0040, i13504)
    order(e0040, b0015, i13504)

Location of a SubComponent
==========================

Here we add base coordinates to SubComponents.
But first, use compute_sequence to get the full sequence for the BBa_I13504 device
See http://parts.igem.org/Part:BBa_I13504

.. code-block:: python

    i13504_seq = compute_sequence(i13504)

compute_sequence added Ranges to the subcomponents. Check one of those ranges to see that the values are what we expect.
The expected range of the terminator is (733, 861).

.. code-block:: python

    b0015_subcomponent = next(f for f in i13504.features if f.instance_of == b0015.identity)
    b0015_range = b0015_subcomponent.locations[0]
    print(f'Range of {b0015.display_name}: ({b0015_range.start}, {b0015_range.end})')

GFP production from expression cassette
=======================================

In this example, we will create a system representation that includes DNA, proteins, and interactions.
First, create the system representation. functional_component creates this for us.

.. code-block:: python

    i13504_system = functional_component('i13504_system')
    doc.add(i13504_system)

The system has two physical subcomponents, the expression construct and the expressed GFP protein. We already created the expression construct. Now create the GFP protein. ed_protein creates an "externally defined protein"

.. code-block:: python

    gfp = add_feature(i13504_system, ed_protein('https://www.fpbase.org/protein/gfpmut3/', name='GFP'))

Now create the part-subpart hierarchy.

.. code-block:: python

    i13504_subcomponent = add_feature(i13504_system, i13504)

Use a ComponentReference to link SubComponents in a multi-level hierarchy.

.. code-block:: python

    e0040_subcomponent = next(f for f in i13504.features if f.instance_of == e0040.identity)
    e0040_reference = ComponentReference(i13504_subcomponent, e0040_subcomponent)
    i13504_system.features.append(e0040_reference)

Make the Interaction.
Interaction type: SBO:0000589 (genetic production)
Participation roles: SBO:0000645 (template), SBO:0000011 (product)

.. code-block:: python

    add_interaction(tyto.SBO.genetic_production,
                participants={gfp: tyto.SBO.product, e0040_reference: tyto.SBO.template})

Concatenating and Reusing Components
====================================

Connecting the i13504_system with promoters to drive expression is much like building i13504: selecting features and ordering them.
First, we create the two promoters:

.. code-block:: python

    J23101_sequence = 'tttacagctagctcagtcctaggtattatgctagc'
    J23101, _ = doc.add(promoter('J23101', sequence=J23101_sequence))
    J23106_sequence = 'tttacggctagctcagtcctaggtatagtgctagc'
    J23106, _ = doc.add(promoter('J23106', sequence=J23106_sequence))

Then we connect them to ComponentReference objects that reference the i13504 SubComponents.

.. code-block:: python

    device1 = doc.add(functional_component('interlab16device1'))
    device1_i13504_system = add_feature(device1, SubComponent(i13504_system))
    order(J23101, ComponentReference(device1_i13504_system, i13504_subcomponent), device1)
    device2 = doc.add(functional_component('interlab16device2'))
    device2_i13504_system = add_feature(device2, SubComponent(i13504_system))
    order(J23106, ComponentReference(device2_i13504_system, i13504_subcomponent), device2)
    print(f'Device 1 second subcomponent points to {device1.constraints[0].object.lookup().refers_to.lookup().instance_of}')

Making a Collection
===================

We will just add the two devices that we built here, not all five on the slide.

.. code-block:: python

    interlab16 = doc.add(Collection('interlab16',members=[device1, device2]))
    print(f'Members are {", ".join(m.lookup().display_id for m in interlab16.members)}')

Creating Strains
================

Describing an engineered strain is much like the other components we have defined, just with different types.
First, we create Component objects for the DH5-a E. coli strain and the backbone vector we will use for the transfection.

.. code-block:: python

    ecoli = doc.add(strain('Ecoli_DH5_alpha'))
    pSB1C3 = doc.add(Component('pSB1C3', SBO_DNA, roles=[tyto.SO.plasmid_vector]))

Now create the engineered strain

.. code-block:: python

    device1_ecoli = doc.add(strain('device1_ecoli'))

Create a local description of the vector as the combination of Device 1 and pSB1C3.

.. code-block:: python

    plasmid = LocalSubComponent(SBO_DNA, roles=[tyto.SO.plasmid_vector], name="Interlab Device 1 in pSB1C3")
    device1_ecoli.features.append(plasmid)
    device1_subcomponent = contains(plasmid, device1)
    contains(plasmid, pSB1C3)
    order(device1, pSB1C3, device1_ecoli)

And put the vector into the transformed strain

.. code-block:: python

    contains(ecoli, plasmid, device1_ecoli)

Defining an abstract interface
==============================

To refer to the GFP, we need to peer down two levels of hierarchy

.. code-block:: python

    gfp_in_i13504_system = add_feature(device1_ecoli, ComponentReference(in_child_of=device1_i13504_system, refers_to=gfp))
    gfp_in_strain = add_feature(device1_ecoli, ComponentReference(in_child_of=device1_subcomponent, refers_to=gfp_in_i13504_system))
    device1_ecoli.interface = Interface(outputs=[gfp_in_strain])

Linking to a Model
==================

.. code-block:: python

    ode_model = doc.add(Model('my_iBioSIM_ODE', 'https://synbiohub...', tyto.EDAM.SBML, tyto.SBO.continuous_framework))
    device1_ecoli.models.append(ode_model)

Describing an experimental condition
====================================

First, define M9 media from its recipe. In this case, unfortunately, tyto has a hard time with ambiguities in the catalog, so we have to look up the PubMed compound IDs directly.

.. code-block:: python

    pubchem_water = 'https://identifiers.org/pubchem.compound:962'
    pubchem_glucose = 'https://identifiers.org/pubchem.compound:5793'
    pubchem_MgSO4 = 'https://identifiers.org/pubchem.compound:24083'
    pubchem_CaCl2 = 'https://identifiers.org/pubchem.compound:5284359'

The media recipe can be expressed using a map from ingredients to Measure objects:

.. code-block:: python

    m9_minimal_media_recipe = {
        LocalSubComponent(SBO_FUNCTIONAL_ENTITY, name="M9 salts"): (20, tyto.OM.milliliter),
        ed_simple_chemical(pubchem_water): (78, tyto.OM.milliliter),
        ed_simple_chemical(pubchem_glucose): (2, tyto.OM.milliliter),
        ed_simple_chemical(pubchem_MgSO4): (200, tyto.OM.microliter),
        ed_simple_chemical(pubchem_CaCl2): (10, tyto.OM.microliter)
    }
    m9_media = doc.add(media("M9_media", m9_minimal_media_recipe))

Then we do the same to describe the sample as a mixture of cells, media, and additional carbon source:

.. code-block:: python

    sample1 = doc.add(functional_component("Sample1"))
    add_feature(sample1, m9_media).measures.append(Measure(200, tyto.OM.microliter, types=tyto.SBO.volume))
    add_feature(sample1, device1_ecoli).measures.append(Measure(10000, tyto.OM.count, types=tyto.SBO.number_of_entity_pool_constituents))
    add_feature(sample1, ed_simple_chemical(pubchem_glucose)).measures.append(Measure(2.5, tyto.OM.milligram, types=tyto.SBO.mass_of_an_entity_pool))

Designing a multi-factor experiment
===================================

Here we will use a CombinatorialDerivation

First, we create the template Component, using LocalSubComponent placeholders for the variables to fill in, following much the same pattern as for the single sample:

.. code-block:: python

    template = doc.add(functional_component("SampleSpec"))
    add_feature(template, m9_media).measures.append(Measure(200, tyto.OM.microliter, types=tyto.SBO.volume))
    sample_strain = add_feature(template, LocalSubComponent(tyto.NCIT.Strain))
    sample_strain.measures.append(Measure(10000, tyto.OM.count, types=tyto.SBO.number_of_entity_pool_constituents))
    sample_carbon_source = add_feature(template, LocalSubComponent(SBO_SIMPLE_CHEMICAL))
    sample_carbon_source.measures.append(Measure(2.5, tyto.OM.milligram, types=tyto.SBO.mass_of_an_entity_pool))

For this, we need our sugars to be Component objects that can be referenced independently from the CombinatorialDerivation, rather than Features:

.. code-block:: python

    pubchem_arabinose = 'https://identifiers.org/pubchem.compound:5460291'
    pubchem_maltose = 'https://identifiers.org/pubchem.compound:6255'
    pubchem_lactose = 'https://identifiers.org/pubchem.compound:6134'

    arabinose = doc.add(Component(url_to_identity(pubchem_arabinose), SBO_SIMPLE_CHEMICAL))
    glucose = doc.add(Component(url_to_identity(pubchem_glucose), SBO_SIMPLE_CHEMICAL))
    maltose = doc.add(Component(url_to_identity(pubchem_maltose), SBO_SIMPLE_CHEMICAL))
    lactose = doc.add(Component(url_to_identity(pubchem_lactose), SBO_SIMPLE_CHEMICAL))

Then we create the derivation itself as a combination of alternatives:

.. code-block:: python

    carbon_source_experiment = CombinatorialDerivation("VaryCarbon", template, strategy=SBOL_ENUMERATE)
    carbon_source_experiment.variable_features = [
        VariableFeature(cardinality=SBOL_ONE, variable=sample_strain, variant_collections=[interlab16]),
        VariableFeature(cardinality=SBOL_ONE, variable=sample_carbon_source, variants=[arabinose, glucose, maltose, lactose])
    ]

Samples in Triplicate
=====================

Each sample is represented by an Implementation, to which we attach and FCS file with flow cytometry data from the sample.

.. code-block:: python

    replicate1 = doc.add(Implementation("Replicate1", built=sample1))
    replicate1.attachments.append(doc.add(Attachment("Replicate1_cytometry_fcs", "https://...")))
    replicate2 = doc.add(Implementation("Replicate2", built=sample1))
    replicate2.attachments.append(doc.add(Attachment("Replicate2_cytometry_fcs", "https://...")))
    replicate3 = doc.add(Implementation("Replicate3", built=sample1))
    replicate3.attachments.append(doc.add(Attachment("Replicate3_cytometry_fcs", "https://...")))

Using Provenance to Connect Design, Build and Test
==================================================

We will show how to do one representative link here:

.. code-block:: python

    measure_sample_1 = doc.add(Activity("measure_sample_1", types=tyto.NCIT.flow_cytometry, usage=Usage(replicate1.identity)))
    doc.find("Replicate1_cytometry_fcs").generated_by.append(measure_sample_1)

Validation
==========

Document.validate returns a validation report. If the report is empty, the document is valid.

.. code-block:: python

    report = doc.validate()
    if report:
        print('Document is not valid')
        print(f'Document has {len(report.errors)} errors')
        print(f'Document has {len(report.warnings)} warnings')
    else:
        print('Document is valid')
