import warnings
from urllib.parse import urlparse

# We probably want to turn this into a dict like the configuration dict
# in pySBOL2. When we have more variables to store, let's change this
# to a dict.
SBOL3_NAMESPACE = ''


def get_namespace() -> str:
    return SBOL3_NAMESPACE


def set_namespace(namespace: str) -> None:
    parsed = urlparse(namespace)
    if parsed.scheme and parsed.netloc:
        global SBOL3_NAMESPACE
        SBOL3_NAMESPACE = namespace
    else:
        raise ValueError(f'Expected URL found {namespace}')


def set_defaults() -> None:
    """Restores configuration to factory settings.
    """
    set_namespace('http://example.com/sbol3/')


set_defaults()


def set_homespace(homespace: str) -> None:
    warnings.warn('Use set_namespace instead', DeprecationWarning)
    return set_namespace(homespace)


def get_homespace() -> str:
    warnings.warn('Use get_namespace instead', DeprecationWarning)
    return get_namespace()
