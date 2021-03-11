import sbol3


class DataSheet(sbol3.CustomIdentified):
    TYPE_URI = 'http://example.org/sbol3#DataSheet'
    RATE_URI = 'http://example.org/sbol3#txRate'

    def __init__(self, rate=None):
        super().__init__(type_uri=DataSheet.TYPE_URI)
        self.transcription_rate = sbol3.FloatProperty(self,
                                                      DataSheet.RATE_URI,
                                                      0, 1,
                                                      initial_value=rate)


class Analysis(sbol3.CustomTopLevel):
    TYPE_URI = 'http://example.org/sbol3#Analysis'
    MODEL_URI = 'http://example.org/sbol3#fittedModel'
    DATA_SHEET_URI = 'http://example.org/sbol3#dataSheet'

    def __init__(self, identity=None, model=None):
        super().__init__(identity=identity,
                         type_uri=Analysis.TYPE_URI)
        self.fitted_model = sbol3.ReferencedObject(self,
                                                   Analysis.MODEL_URI,
                                                   0, 1,
                                                   initial_value=model)
        self.data_sheet = sbol3.OwnedObject(self,
                                            Analysis.DATA_SHEET_URI,
                                            0, 1,
                                            type_constraint=DataSheet)


# Register the constructor with the parser
sbol3.Document.register_builder(DataSheet.TYPE_URI, DataSheet)
sbol3.Document.register_builder(Analysis.TYPE_URI, Analysis)
