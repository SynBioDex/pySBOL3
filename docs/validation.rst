Validation in pySBOL3
=============================

The pySBOL3 library includes a capability to generate a validation
report for an SBOL3 object or an SBOL3 Document. The report can be
used to check your work or fix issues with your document or object.

Here is a short example of how to validate an object. We intentionally
create a Range with end before start, which is invalid SBOL3. This
generates a validation error in the ValidationReport:

.. code:: python

    >>> import sbol3
    RDFLib Version: 5.0.0
    >>> seq_uri = 'https://github.com/synbiodex/pysbol3/sequence'
    >>> start = 10
    >>> end = 1
    >>> r = sbol3.Range(seq_uri, start, end)
    >>> report = r.validate()
    >>> len(report)
    1
    >>> for error in report.errors:
    ...     print(error.message)
    ...
    sbol3-11403: Range.end must be >= start

.. end

Validating an object automatically validates and child objects. Invoking `validate()`
on a document will validate all objects contained in that document.
