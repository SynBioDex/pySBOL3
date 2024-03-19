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

Using the Data Model
====================

Import Modules
--------------

.. code-block:: python

    from sbol3 import *
    from sbol_utilities.calculate_sequences import compute_sequence
    from sbol_utilities.component import *
    from sbol_utilities.helper_functions import url_to_identity
    import tyto

Set Default Namespace and Create Document
-----------------------------------------

.. code-block:: python

    set_namespace('https://synbiohub.org/public/igem/')
    doc = Document()

Create and Add Components
-------------------------

Example: Creating a GFP Expression Cassette

.. code-block:: python

    i13504 = Component('i13504', SBO_DNA)
    i13504.name = 'iGEM 2016 interlab reporter'
    i13504.description = 'GFP expression cassette used for 2016 iGEM interlab study'
    i13504.roles.append(tyto.SO.engineered_region)
    doc.add(i13504)

Construct Part-Subpart Hierarchy
--------------------------------

.. code-block:: python

    b0034, b0034_seq = doc.add(rbs('B0034', sequence='aaagaggagaaa', name='RBS (Elowitz 1999)'))
    e0040_sequence = '...'
    e0040, _ = doc.add(cds('E0040', sequence=e0040_sequence, name='GFP'))
    b0015_sequence = '...'
    b0015, _ = doc.add(terminator('B0015', sequence=b0015_sequence, name='double terminator'))

    order(b0034, e0040, i13504)
    order(e0040, b0015, i13504)

Linking Components with Interactions
------------------------------------

.. code-block:: python

    i13504_system = functional_component('i13504_system')
    doc.add(i13504_system)

    gfp = add_feature(i13504_system, ed_protein('https://www.fpbase.org/protein/gfpmut3/', name='GFP'))
    i13504_subcomponent = add_feature(i13504_system, i13504)

    e0040_subcomponent = next(f for f in i13504.features if f.instance_of == e0040.identity)
    e0040_reference = ComponentReference(i13504_subcomponent, e0040_subcomponent)
    i13504_system.features.append(e0040_reference)

    add_interaction(tyto.SBO.genetic_production,
                    participants={gfp: tyto.SBO.product, e0040_reference: tyto.SBO.template})


Working with SubComponent Locations
-----------------------------------------

In order to specify the exact range (start and end positions) on the parent component sequence where the child
component is located, use the ``Range`` class. The ``Range`` class takes two required arguments, ``start`` and
``end``, which are the start and end positions of the child component on the parent component sequence.
The ``Range`` class also takes an optional argument, ``sequence``, which is the sequence of the child component.
The ``Range`` class is then used as the value of the ``locations`` attribute of the ``SubComponent``.
Example for a DNA component with a DNA SubComponent:

.. code:: python

    start = 1
    end = 4
    sub_sequence = sbol3.Sequence("LysineCodon", elements=b0034_seq.elements[start - 1 : end - 1])
    range_location = sbol3.Range(start=start, end=end, sequence=sub_sequence)
    subcomponent = sbol3.SubComponent(gfp, name="LysineCodon", roles=[tyto.SO.codon], locations=range_location)

.. end

Document Validation
-------------------

.. code-block:: python

    report = doc.validate()
    if report:
        print('Document is not valid')
        print(f'Document has {len(report.errors)} errors')
        print(f'Document has {len(report.warnings)} warnings')
    else:
        print('Document is valid')

Exporting the Document
----------------------

.. code-block:: python

    doc.write('i13504.nt', file_format=SORTED_NTRIPLES)
