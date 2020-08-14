from urllib.parse import urlparse

# We probably want to turn this into a dict like the configuration dict
# in pySBOL2. When we have more variables to store, let's change this
# to a dict.
SBOL3_HOMESPACE = ''


def get_homespace() -> str:
    return SBOL3_HOMESPACE


def set_homespace(homespace: str) -> None:
    parsed = urlparse(homespace)
    if parsed.scheme and parsed.netloc and parsed.path:
        global SBOL3_HOMESPACE
        SBOL3_HOMESPACE = homespace
    else:
        raise ValueError(f'Expected URL found {homespace}')


def set_defaults() -> None:
    """Restores configuration to factory settings.
    """
    set_homespace('http://example.com/sbol3/')


set_defaults()
