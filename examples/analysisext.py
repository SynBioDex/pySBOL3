import sbol3


class Analysis(sbol3.TopLevel):

    TYPE_URI = 'http://examples.org#Analysis'
    FITTED_MODEL_URI = 'http://example.org/sbol3#fit'

    def __init__(self, identity=None, model=None,
                 *, type_uri=TYPE_URI):
        # Override the default type_uri that is used when serializing
        super().__init__(identity=identity, type_uri=type_uri)
        self.fittedModel = sbol3.ReferencedObject(self,
                                                  Analysis.FITTED_MODEL_URI,
                                                  0, 1,
                                                  initial_value=model)


# Register the constructor with the parser
sbol3.Document.register_builder(Analysis.TYPE_URI, Analysis)
