import warnings
from typing import Optional
from urllib.parse import urlparse

# We probably want to turn this into a dict like the configuration dict
# in pySBOL2. When we have more variables to store, let's change this
# to a dict.
SBOL3_NAMESPACE = None


def get_namespace() -> Optional[str]:
    return SBOL3_NAMESPACE


def set_namespace(namespace: Optional[str]) -> None:
    global SBOL3_NAMESPACE
    if namespace is None:
        SBOL3_NAMESPACE = None
        return
    parsed = urlparse(namespace)
    if parsed.scheme and parsed.netloc:
        SBOL3_NAMESPACE = namespace
    else:
        raise ValueError(f'Expected URL, found {namespace}')


def set_defaults() -> None:
    """Restores configuration to factory settings.
    """
    set_namespace(None)


set_defaults()
