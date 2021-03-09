import sbol3

X_COORDINATE_URI = 'http://example.org/my_vis#x_coordinate'
Y_COORDINATE_URI = 'http://example.org/my_vis#y_coordinate'


class ComponentExtension(sbol3.Component):

    # Note that a no-argument constructor is defined using a default URI
    def __init__(self, identity, types,
                 *, type_uri=sbol3.SBOL_COMPONENT):
        super().__init__(identity=identity, types=types, type_uri=type_uri)
        self.x_coordinate = sbol3.IntProperty(self, X_COORDINATE_URI, 0, 1,
                                              initial_value=0)
        self.y_coordinate = sbol3.IntProperty(self, Y_COORDINATE_URI, 0, 1,
                                              initial_value=0)


def build_component_extension(*, identity, type_uri):
    # Types is required and not known at build time.
    # Supply a missing value to the constructor, then clear
    # the missing value before returning the built object.
    obj = ComponentExtension(identity=identity,
                             types=[sbol3.PYSBOL3_MISSING],
                             type_uri=type_uri)
    # Remove the dummy value
    obj.clear_property(sbol3.SBOL_TYPE)
    return obj


sbol3.Document.register_builder(sbol3.SBOL_COMPONENT,
                                build_component_extension)
