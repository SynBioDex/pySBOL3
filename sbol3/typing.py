from __future__ import annotations

from typing import List, Sequence, Union

from .property_base import Property

# URIProperty typing
uri_list = Union[List[str], Property]
uri_singleton = Union[str, Property]

# Owned object property
ownedobj = 'Identified'
ownedobj_list = Sequence['Identified']
ownedobj_list_arg = Union[ownedobj, ownedobj_list]

# ReferencedObject
refobj = Union['Identified', str]
refobj_list = Sequence[refobj]
refobj_list_arg = Union[refobj, refobj_list]
