from typing import Sequence


class ValidationError:
    """A ValidationError is a violation of the SBOL specification.
    """

    def __init__(self, object_id, rule_id, message):
        self.rule_id = rule_id
        self.message = message
        self.object_id = object_id

    def __str__(self):
        result = f'{self.rule_id}: {self.message}'
        if self.object_id is not None:
            result = f'{self.object_id} {result}'
        return result


class ValidationWarning:
    """A ValidationWarning is a violation of an SBOL best practice.
    """

    def __init__(self, object_id, rule_id, message):
        self.rule_id = rule_id
        self.message = message
        self.object_id = object_id


class ValidationReport:

    def __init__(self):
        self._errors = []
        self._warnings = []

    def __len__(self):
        return len(self._errors) + len(self._warnings)

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
