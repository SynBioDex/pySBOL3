import argparse
import logging
from typing import Any

import sbol3

# This example demonstrates how to adapt the functional vistor pattern
# in pySBOL3 to an object oriented visitor pattern similar to
# https://refactoring.guru/design-patterns/visitor/python/example or
# https://en.wikipedia.org/wiki/Visitor_pattern#Python_example

# Usage:
#
#    python3 visitor.py [-d] SBOL_FILE_NAME


class SBOLVisitor:
    """A base class for visitor pySBOL3 visitors.
    """

    def __call__(self, sbol_object: sbol3.Identified):
        """This method is invoked on every SBOL object that is visited. The
        visit is then dispatched to a type-specific method. If no
        type-specific method exists, `visit_fallback` is invoked with
        the SBOL object. The default implementation of
        `visit_fallback` does nothing.

        """
        method_name = self._method_name(sbol_object)
        try:
            getattr(self, method_name)(sbol_object)
        except AttributeError:
            self.visit_fallback(sbol_object)

    def _method_name(self, thing: Any) -> str:
        """Generates a visitor method name for a given object. Override this
        method if you want a different conversion from object to
        method name.

        """
        qualname = type(thing).__qualname__.replace(".", "_")
        return f'visit_{qualname}'

    def visit_fallback(self, sbol_object: sbol3.Identified):
        """Visit an object that doesn't have a specific method for its type.
        Override this method to catch objects that do not have a
        specific visit method defined for them.

        """
        pass


class MyVisitor(SBOLVisitor):
    """An example visitor.

    """

    def visit_Component(self, c):
        print(f'Visited Component {c.identity}')

    def visit_SubComponent(self, sc):
        print(f'Visited SubComponent {sc.identity}')

    def visit_fallback(self, sbol_object: sbol3.Identified):
        type_name = type(sbol_object).__qualname__
        logging.debug(f'Fallback visit of {type_name} {sbol_object.identity}')


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
    doc.traverse(my_visitor)


if __name__ == '__main__':
    main()
