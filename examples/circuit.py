import sbol3

# This example encodes a circuit depicted at
# https://github.com/BuildACell/BioCRNPyler/blob/master/README.md

sbol3.set_namespace('https://github.com/BuildACell/BioCRNPyler')

# Ptet promoter
ptet = sbol3.Component('pTetR', sbol3.SBO_DNA)
ptet.roles = [sbol3.SO_PROMOTER]
ptet.name = 'pTetR'
ptet.description = 'TetR repressible promoter'

# The operator
op1 = sbol3.Component('op1', sbol3.SBO_DNA)
op1.roles = [sbol3.SO_OPERATOR]
op1.description = 'Your Description Here'

# RBS
utr1 = sbol3.Component('UTR1', sbol3.SBO_DNA)
utr1.roles = [sbol3.SO_RBS]
utr1.description = 'Your Description Here'

# Create the GFP coding sequence
gfp = sbol3.Component('GFP', sbol3.SBO_DNA)
gfp.roles.append(sbol3.SO_CDS)
gfp.name = 'GFP'
gfp.description = 'GFP Coding Sequence'

# Wrap it together
circuit = sbol3.Component('circuit', sbol3.SBO_DNA)
circuit.roles.append(sbol3.SO_ENGINEERED_REGION)
ptet_sc = sbol3.SubComponent(ptet)
op1_sc = sbol3.SubComponent(op1)
utr1_sc = sbol3.SubComponent(utr1)
gfp_sc = sbol3.SubComponent(gfp)

# circuit.features can be set and appended to like any Python list
circuit.features = [ptet_sc, op1_sc]
circuit.features += [utr1_sc]
circuit.features.append(gfp_sc)

circuit.constraints = [sbol3.Constraint(sbol3.SBOL_PRECEDES, ptet_sc, op1_sc),
                       sbol3.Constraint(sbol3.SBOL_PRECEDES, op1_sc, utr1_sc),
                       sbol3.Constraint(sbol3.SBOL_PRECEDES, utr1_sc, gfp_sc)]

doc = sbol3.Document()
# TODO: Enhancement: doc.addAll([ptet, op1, utr1, ...])
doc.add(ptet)
doc.add(op1)
doc.add(utr1)
doc.add(gfp)
doc.add(circuit)
doc.write('circuit.nt', sbol3.SORTED_NTRIPLES)
