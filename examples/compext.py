import sbol3

X_COORDINATE_URI = 'http://example.org/my_vis#x_coordinate'
Y_COORDINATE_URI = 'http://example.org/my_vis#y_coordinate'


class ComponentExtension(sbol3.Component):
    """Override sbol3.Component to add two fields
    for visual display.
    """

    def __init__(self, identity, types,
                 *, type_uri=sbol3.SBOL_COMPONENT):
        super().__init__(identity=identity, types=types, type_uri=type_uri)
        self.x_coordinate = sbol3.IntProperty(self, X_COORDINATE_URI, 0, 1,
                                              initial_value=0)
        self.y_coordinate = sbol3.IntProperty(self, Y_COORDINATE_URI, 0, 1,
                                              initial_value=0)


def build_component_extension(*, identity, type_uri):
    """A builder function to be called by the SBOL3 parser
    when it encounters a Component in an SBOL file.
    """

    # `types` is required and not known at build time.
    # Supply a missing value to the constructor, then clear
    # the missing value before returning the built object.
    obj = ComponentExtension(identity=identity,
                             types=[sbol3.PYSBOL3_MISSING],
                             type_uri=type_uri)
    # Remove the dummy value
    obj.clear_property(sbol3.SBOL_TYPE)
    return obj


# Register the builder function so it can be invoked by
# the SBOL3 parser to build objects with a Component type URI
sbol3.Document.register_builder(sbol3.SBOL_COMPONENT,
                                build_component_extension)
