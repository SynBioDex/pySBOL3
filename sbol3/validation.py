from typing import Sequence

# TODO: Find all calls to super validate, make sure they pass report
#    grep super sbol3/*.py | grep validate
# TODO: Deconflict error.ValidationError and validation.ValidationError


class ValidationError:

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ValidationWarning:

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ValidationReport:

    def __init__(self):
        self._errors = []
        self._warnings = []

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
