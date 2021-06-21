import posixpath
import unittest

import sbol3


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_default_namespace(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/263
        display_id = 'foo'
        c = sbol3.Component(display_id, sbol3.SBO_DNA)
        self.assertIsNotNone(c.namespace)
        self.assertTrue(c.identity.endswith(display_id))
        self.assertEqual(c.identity, posixpath.join(c.namespace, display_id))


if __name__ == '__main__':
    unittest.main()
