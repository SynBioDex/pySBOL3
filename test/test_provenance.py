import unittest

import sbol3


class TestActivity(unittest.TestCase):

    def test_create(self):
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


class TestAgent(unittest.TestCase):

    def test_create(self):
        display_id = 'agent'
        agent = sbol3.Agent(display_id)
        self.assertIsNotNone(agent)
        self.assertEqual(display_id, agent.display_id)
        # attachments come from TopLevel
        self.assertEqual([], agent.attachments)


class TestAssociation(unittest.TestCase):

    def test_create(self):
        agent = sbol3.Agent('agent')
        association = sbol3.Association(agent)
        self.assertIsNotNone(association)
        self.assertEqual([], association.roles)
        self.assertEqual(None, association.plan)
        self.assertEqual(agent.identity, association.agent)


class TestPlan(unittest.TestCase):

    def test_create(self):
        display_id = 'plan'
        plan = sbol3.Plan(display_id)
        self.assertIsNotNone(plan)
        self.assertEqual(display_id, plan.display_id)
        # attachments come from TopLevel
        self.assertEqual([], plan.attachments)


class TestUsage(unittest.TestCase):

    def test_create(self):
        agent = sbol3.Agent('agent')
        usage = sbol3.Usage(agent.identity)
        self.assertIsNotNone(usage)
        self.assertEqual(agent.identity, usage.entity)
        self.assertEqual([], usage.roles)


if __name__ == '__main__':
    unittest.main()
