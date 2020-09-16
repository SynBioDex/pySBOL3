Design Decisions
================

URIs
----

The sbol Python module uses `rdflib.URIRef
<https://rdflib.readthedocs.io/en/stable/rdf_terms.html#urirefs>`_ as
the core type of all URI-like items. This is a change from the C++
based pysbol module, which represented URIs as strings. As a result of
this design choice, some constructs that might have worked in the past
will no longer work. We made a conscious choice to break backward
compatiblity in order to properly type the URIs.

The pure python module is internally consistent with respect to
URIs. The constants that are defined by the sbol module are of type
``rdflib.URIRef`` instead of ``str``. Code that ignored those constants
and defined URIs as strings may break in some cases.

For example, code defined as follows will no longer work:

.. code-block:: python

    TYPE_PRODUCERS = ['http://identifiers.org/biomodels.sbo/SBO:0000589']

    if interaction.types[0] in TYPE_PRODUCERS:
        print(interaction.identity)


Instead, the defined constant can be used for a clearer list of
producers and for compatibility with both the C++ based pysbol module
and with the pure python sbol module:

.. code-block::	python

    TYPE_PRODUCERS = [sbol.SBO_GENETIC_PRODUCTION]

    if interaction.types[0] in TYPE_PRODUCERS:
        print(interaction.identity)


Where a defined constant is not available, an ``rdflib.URIRef`` should be
used:

.. code-block::	python

    TYPE_PRODUCERS = [rdflib.URIRef('http://example.org/example/PRODUCER')]

    if interaction.types[0] in TYPE_PRODUCERS:
        print(interaction.identity)
