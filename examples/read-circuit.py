import sbol3

# A short example to demonstrate reading the file generated
# by pySBOL3/examples/circuit.py

doc = sbol3.Document()
doc.read('circuit.nt')
# Find the circuit by display_id
circuit = doc.find('circuit')
# Print the circuit's full URI
print(circuit.identity)

# Iterate over the circuit's features
for f in circuit.features:
    print(f)
    if isinstance(f, sbol3.SubComponent):
        sc = f
        # This gets the URI
        print(sc.instance_of)
        # This gets the object that instance_of points to
        print(sc.instance_of.lookup())
    print()

# Print out all of the circuit's constraints
for c in circuit.constraints:
    print(f'{c.subject} {c.restriction} {c.object}')
