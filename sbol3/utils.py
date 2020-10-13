# Functions that don't fit anywhere else.

def parse_class_name(uri: str):
    """Parse the class name in a URI.

    The input is expected to be of the form 'http://sbols.org/v3#Component'
    or 'http://example.com/ApplicationSpecificClass'. This function would
    return 'Component' and 'ApplicationSpecificClass' respectively.
    """
    if '#' in uri:
        return uri[uri.rindex('#')+1:]
    elif '/' in uri:
        return uri[uri.rindex('/')+1:]
    raise ValueError(f'Cannot parse class name from {uri}. URI must use either / '
                     'or # as a delimiter.')
