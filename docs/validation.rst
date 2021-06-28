Validation in pySBOL3
=============================

-----------------------------
Validating Documents
-----------------------------

The most common use of validation will be validating entire
documents. After objects have been loaded, created, or manipulated, a
programmer can invoke `validate` on the `Document` to get a report of
any errors or warnings. If the length of the report is 0, or if the
report evaluates to boolean False, there are no validation issues. If
there are validation issues it is possible to iterate over the
validation errors and warnings as show in the next section.

Here is an example that validates a newly loaded document:

.. code:: python

    >>> import sbol3
    RDFLib Version: 5.0.0
    >>> doc = sbol3.Document()
    >>> doc.read('combine2020.ttl')
    >>> report = doc.validate()
    >>> len(report)
    0
    >>> bool(report)
    False

.. end


-----------------------------
Validating Objects
-----------------------------

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
    >>> bool(report)
    True
    >>> for error in report.errors:
    ...     print(error.message)
    ...
    sbol3-11403: Range.end must be >= start

.. end

Validating an object automatically validates any child
objects. Invoking `validate()` on a document will validate all objects
contained in that document.

-----------------------------
Extending Validation
-----------------------------

If you are building extension classes and want to add custom
validation to those objects you can extend the pySBOL3 validation in
your custom classes. To do so, define your own `validate` method, call
the super method, then perform your own validation, adding warnings or
errors to the validation report. Finally, your `validate` method must
return the `ValidationReport` to the caller. This new method will
automatically get called when a `Document` is validated or when the an
instance of this class is validated.

Here is an example:

.. code:: python

    def validate(self, report: ValidationReport = None) -> ValidationReport:

        # Invoke the super method, and hold on to the resulting report
        report = super().validate(report)

        # Run my own validation here
        if self.x >= self.x2:
	    report.addError(self.identity, None, 'X must be less than X2')
	if self.x > 100:
	    report.addWarning(self.identity, None, 'X values over 100 do not work well')

	# Return the report to the caller
        return report

.. end
