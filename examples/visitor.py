import argparse
import logging

import sbol3

# This example demonstrates how to use the visitor pattern
# in pySBOL3 to navigate a document
#
# Usage:
#
#    python3 visitor.py [-d] SBOL_FILE_NAME


class MyVisitor:
    """An example visitor.

    """

    def visit_document(self, doc: sbol3.Document):
        for obj in doc.objects:
            obj.accept(self)

    def visit_component(self, c: sbol3.Component):
        for feature in c.features:
            feature.accept(self)
        print(f'Visited Component {c.identity}')

    def visit_component_reference(self, cr: sbol3.ComponentReference):
        print(f'Visited ComponentReference {cr.identity}')

    def visit_sub_component(self, sc: sbol3.SubComponent):
        print(f'Visited SubComponent {sc.identity}')


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", metavar="SBOL_FILE")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def main(argv=None):
    args = parse_args(argv)
    init_logging(args.debug)
    doc = sbol3.Document()
    doc.read(args.inputfile)
    my_visitor = MyVisitor()
    doc.accept(my_visitor)


if __name__ == '__main__':
    main()
