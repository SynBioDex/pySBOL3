from typing import Sequence


class ValidationError:
    """A ValidationError is a violation of the SBOL specification.
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ValidationWarning:
    """A ValidationWarning is a violation of an SBOL best practice.
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message


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

    def addError(self, code, message):
        self._errors.append(ValidationError(code, message))

    def addWarning(self, code, message):
        self._warnings.append(ValidationWarning(code, message))
