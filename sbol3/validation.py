from typing import Sequence


class ValidationIssue:
    """Base class for ValidationError and ValidationWarning.
    """

    def __init__(self, object_id, rule_id, message):
        self.rule_id = rule_id
        self.message = message
        self.object_id = object_id

    def __str__(self):
        if self.object_id and self.rule_id:
            return f'{self.object_id} {self.rule_id}: {self.message}'
        elif self.object_id:
            return f'{self.object_id}: {self.message}'
        elif self.rule_id:
            return f'{self.rule_id}: {self.message}'
        else:
            return self.message


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
        for error in self._errors:
            yield error
        for warning in self._warnings:
            yield warning

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
