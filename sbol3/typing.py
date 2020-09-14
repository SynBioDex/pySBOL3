from typing import Union, List

from .property_base import Property

# URIProperty typing
uri_list = Union[List[str], Property]
uri_singleton = Union[str, Property]
# Owned object property
oo_list = Union[List['Identified'], Property]
