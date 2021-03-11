Using Ontology Terms
====================

SBOL leans heavily on a variety of ontologies for
terminology. Examples include `PROV-O
<https://www.w3.org/TR/prov-o/>`_ for provenance terms, and `Ontology
of units of Measure <https://www.ebi.ac.uk/ols/ontologies/om>`_ for
defining and using measures and units.  The most commonly used terms
are defined as pySBOL3 constants. These only scratch the surface of
what is available.

`TYTO <https://github.com/SynBioDex/tyto>`_ is a Python module that
automates the lookup of ontology terms so that you do not have to
remember long, sometimes meaningless URIs. Here is an example of
ontology lookup using TYTO:

.. code:: python

    >>> import tyto
    RDFLib Version: 5.0.0
    >>> tyto.SO.promoter
    'https://identifiers.org/SO:0000167'
    >>> tyto.SBO.systems_biology_representation
    'https://identifiers.org/SBO:0000000'

.. end

TYTO and pySBOL3 will happily coexist and work together.  TYTO can be
used to look up some of the same terms that pySBOL3 defines as
constants. For example:

.. code:: python

    >>> import sbol3
    RDFLib Version: 5.0.0
    >>> import tyto
    >>> sbol3.SBO_DNA == tyto.SBO.deoxyribonucleic_acid
    True
    >>> sbol3.SBO_RNA == tyto.SBO.ribonucleic_acid
    True
    >>> sbol3.SO_PROMOTER == tyto.SO.promoter
    True

.. end


TYTO Installation
-----------------

TYTO can be installed using `pip <https://pypi.org/project/pip/>`_, Python's package installer.

.. code:: shell

    pip install tyto

.. end
