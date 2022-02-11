import unittest

import sbol3


class TestActivity(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'activity'
        activity = sbol3.Activity(display_id)
        self.assertIsNotNone(activity)
        self.assertEqual(display_id, activity.display_id)
        # attachments come from TopLevel
        self.assertEqual([], activity.attachments)
        self.assertEqual([], activity.types)
        self.assertEqual(None, activity.start_time)
        self.assertEqual(None, activity.end_time)
        self.assertEqual([], activity.usage)
        self.assertEqual([], activity.association)

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_type = sbol3.SBOL_DESIGN
        activity1 = sbol3.Activity('activity1', types=test_type)
        self.assertEqual([test_type], activity1.types)


class TestAgent(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'agent'
        agent = sbol3.Agent(display_id)
        self.assertIsNotNone(agent)
        self.assertEqual(display_id, agent.display_id)
        # attachments come from TopLevel
        self.assertEqual([], agent.attachments)


class TestAssociation(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        agent = sbol3.Agent('agent')
        association = sbol3.Association(agent)
        self.assertIsNotNone(association)
        self.assertEqual([], association.roles)
        self.assertEqual(None, association.plan)
        self.assertEqual(agent.identity, association.agent)

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        agent_uri = 'https://example.org/agent'
        role_uri = 'https://example.org/agent_role'
        assoc1 = sbol3.Association(agent=agent_uri, roles=role_uri)
        self.assertEqual([role_uri], assoc1.roles)


class TestPlan(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        display_id = 'plan'
        plan = sbol3.Plan(display_id)
        self.assertIsNotNone(plan)
        self.assertEqual(display_id, plan.display_id)
        # attachments come from TopLevel
        self.assertEqual([], plan.attachments)


class TestUsage(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        agent = sbol3.Agent('agent')
        usage = sbol3.Usage(agent.identity)
        self.assertIsNotNone(usage)
        self.assertEqual(agent.identity, usage.entity)
        self.assertEqual([], usage.roles)

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        entity_uri = 'https://example.org/entity'
        role_uri = 'https://example.org/entity_usage'
        usage1 = sbol3.Usage(entity=entity_uri, roles=role_uri)
        self.assertEqual([role_uri], usage1.roles)


if __name__ == '__main__':
    unittest.main()
