from collections import defaultdict


class SBOLObject:

    def __init__(self) -> None:
        self.properties = defaultdict(list)
        self.owned_objects = defaultdict(list)
        # Does this need to be a property? It does not get serialized to the RDF file.
        # Could it be an attribute that gets composed on the fly? Keep it simple for
        # now, and change to a property in the future if needed.
        self.identity = None
        self.document = None

    def __setattr__(self, name, value):
        try:
            self.__dict__[name].set(value)
        except AttributeError:
            # Attribute set does not exist
            object.__setattr__(self, name, value)
        except KeyError:
            # property name does not exist
            object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        # Call the default method
        result = object.__getattribute__(self, name)
        if hasattr(result, '_sbol_singleton'):
            result = result.get()
        return result

    def validate(self) -> None:
        # We could validate the identity here, but there aren't any
        # particular rules for an SBOLObject.
        pass
