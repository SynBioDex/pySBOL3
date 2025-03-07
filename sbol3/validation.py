from typing import Sequence


class ValidationIssue:
    """Base class for ValidationError and ValidationWarning.
    """

    def __init__(self, object_id, rule_id, message):
        self.rule_id = rule_id
        self.message = message
        self.object_id = object_id

    def __str__(self):
        parts = [] # list of parts to include in the message

        if self.object_id:
            parts.append(str(self.object_id)) # add the object ID if present
        if self.rule_id:
            parts.append(str(self.rule_id)) # add the rule ID if present if present

        # return the message with the parts if parts exits otherwise just the message
        return f"{' '.join(parts)}: {self.message}" if parts else self.message


class ValidationError(ValidationIssue):
    """A ValidationError is a violation of the SBOL specification.
    """
    # All functionality is in the base class
    pass


class ValidationWarning(ValidationIssue):
    """A ValidationWarning is a violation of an SBOL best practice.
    """
    # All functionality is in the base class
    pass


class ValidationReport:

    def __init__(self):
        self._errors = []
        self._warnings = []

    def __len__(self):
        return len(self._errors) + len(self._warnings)

    def __iter__(self):
        yield from self._errors
        yield from self._warnings

    def __str__(self):
        issues = self._errors + self._warnings
        return '\n'.join([str(i) for i in issues])

    @property
    def warnings(self) -> Sequence[ValidationWarning]:
        return tuple(self._warnings)

    @property
    def errors(self) -> Sequence[ValidationError]:
        return tuple(self._errors)

    def addError(self, object_id, rule_id, message):
        self._errors.append(ValidationError(object_id, rule_id, message))

    def addWarning(self, object_id, rule_id, message):
        self._warnings.append(ValidationWarning(object_id, rule_id, message))
