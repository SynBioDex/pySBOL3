Using Visitors
==============

The Visitor Pattern is a well known and commonly used pattern for
performing an operation on the elements of an object structure. There
are many online resources for learning about the visitor pattern.

The implementation of the Visitor Pattern in pySBOL3 is very
simple. When a pySBOL3 object's `accept` method is called, a visitor
is passed as the only arugment. The `accept` method, in turn, invokes
`visit_type` on the visitor, passing the pySBOL3 object as the only
argument.

Traversal of the pySBOL3 object graph is left to the visitor
itself. When a `visit_type` method is called, the visitor must then
invoke `accept` on any child objects it might want to visit. See the
code sample below for an example of this traversal.


Resources
---------
* https://sourcemaking.com/design_patterns/visitor
* https://refactoring.guru/design-patterns/visitor
* https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780201633610


Example Code
------------

The program below will visit each top level object in the document as
well as visiting any features on the top level components. Note that
the visitor must direct the traversal of the features, as discussed
above.

.. code:: python

  import sbol3


  class MyVisitor:

      def visit_component(self, c: sbol3.Component):
          print(f'Component {c.identity}')
          for f in c.features:
              f.accept(self)

      def visit_sequence(self, s: sbol3.Component):
          print(f'Sequence {s.identity}')

      def visit_sub_component(self, sc: sbol3.Component):
          print(f'SubComponent {sc.identity}')


  doc = sbol3.Document()
  doc.read('test/SBOLTestSuite/SBOL3/BBa_F2620_PoPSReceiver/BBa_F2620_PoPSReceiver.ttl')
  visitor = MyVisitor()
  for obj in doc.objects:
      obj.accept(visitor)
.. end


Visit Methods
-------------

The table below lists each class that has an accept method and the
corresponding method that is invoked on the visitor passed to the
accept method.

=======================  ============
Class                    Visit Method
=======================  ============
Activity                 visit_activity
Agent                    visit_agent
Association              visit_association
Attachment               visit_attachment
BinaryPrefix             visit_binary_prefix
Collection               visit_collection
CombinatorialDerivation  visit_combinatorial_derivation
Component                visit_component
ComponentReference       visit_component_reference
Constraint               visit_constraint
Cut                      visit_cut
Document                 visit_document(self)
EntireSequence           visit_entire_sequence
Experiment               visit_experiment
ExperimentalData         visit_experimental_data
ExternallyDefined        visit_externally_defined
Implementation           visit_implementation
Interaction              visit_interaction
Interface                visit_interface
LocalSubComponent        visit_local_sub_component
Measure                  visit_measure
Model                    visit_model
Participation            visit_participation
Plan                     visit_plan
PrefixedUnit             visit_prefixed_unit
Range                    visit_range
SIPrefix                 visit_si_prefix
Sequence                 visit_sequence
SequenceFeature          visit_sequence_feature
SingularUnit             visit_singular_unit
SubComponent             visit_sub_component
UnitDivision             visit_unit_division
UnitExponentiation       visit_unit_exponentiation
UnitMultiplication       visit_unit_multiplication
Usage                    visit_usage
VariableFeature          visit_variable_feature
=======================  ============
