import unicodedata


def string_to_display_id(name: str) -> str:
    """Convert a string to a valid display id.

    The SBOL specification has rules about what constitutes a valid
    display id. Make an effort here to convert any string into a valid
    display id.
    """
    # Contributed via https://github.com/SynBioDex/pySBOL3/issues/191
    def sanitize_character(c):
        # Replace certain characters with underscore
        # Feel free to expand this let
        replacements = {' ', '-', '.', ':', '/', '\\'}
        if c in replacements:
            c = '_'
        # Keep all alphanumerics and underscores
        if c.isalnum() or c == '_':
            # keep allowed characters
            return c
        # all others are changed into a reduced & compatible form
        # of their unicode name
        return f'_{unicodedata.name(c).replace(" SIGN", "").replace(" ", "_")}'

    # make replacements in order to get a compliant displayID
    display_id = ''.join([sanitize_character(c) for c in name.strip()])
    # prepend underscore if there is an initial digit
    if display_id[0].isdigit():
        display_id = '_' + display_id
    return display_id
