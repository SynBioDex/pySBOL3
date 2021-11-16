from __future__ import annotations

import math
import unittest
from typing import Optional

import sbol3


# Define an extension class that includes a text property whose max
# cardinality is greater than 1 to test auto-conversion of strings to
# lists.
class TextPropertyExtension(sbol3.CustomTopLevel):
    TYPE_URI = 'https://github.com/synbiodex/pysbol3/TextPropertyExtension'
    TPE_INFO_URI = 'https://github.com/synbiodex/pysbol3/information'

    def __init__(self, identity,
                 *, information: Optional[str, list[str]] = None,
                 namespace: str = None,
                 attachments: list[str] = None,
                 name: str = None, description: str = None,
                 derived_from: list[str] = None,
                 generated_by: list[str] = None,
                 measures: list[sbol3.SBOLObject] = None) -> None:
        super().__init__(identity=identity,
                         type_uri=TextPropertyExtension.TYPE_URI,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.information = sbol3.TextProperty(self,
                                              TextPropertyExtension.TPE_INFO_URI,
                                              0, math.inf,
                                              initial_value=information)


class TestTextProperty(unittest.TestCase):

    def test_text_list_property(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        # Test initializing with None
        tpe1 = TextPropertyExtension('tpe1')
        self.assertEqual([], tpe1.information)
        # Test initializing with a list
        info_value = ['foo', 'bar']
        tpe2 = TextPropertyExtension('tpe2', information=info_value)
        self.assertListEqual(info_value, list(tpe2.information))
        # Test initializing with a string, which should be marshalled into a list
        info_value = 'foo'
        tpe3 = TextPropertyExtension('tpe3', information=info_value)
        self.assertListEqual([info_value], list(tpe3.information))


if __name__ == '__main__':
    unittest.main()
