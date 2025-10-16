import unittest
from src.agent import Agent, HemisphereA, HemisphereB, HemisphereC

class TestAgent(unittest.TestCase):

    def test_agent_creation(self):
        agent = Agent(
            name="Test Agent",
            role="Tester",
            employee_id="12345",
            hourly_rate=50.0,
            physical_description="A test agent.",
            skill_matrix=["testing"],
            knowledge_sources=["internal"],
            tool_access=["unittest"]
        )
        self.assertEqual(agent.name, "Test Agent")
        self.assertIsInstance(agent.hemisphere_a, HemisphereA)
        self.assertIsInstance(agent.hemisphere_b, HemisphereB)
        self.assertIsInstance(agent.hemisphere_c, HemisphereC)

    def test_decision_process(self):
        agent = Agent("Test Agent", "Tester", "12345", 50.0, "A test agent.", ["testing"], ["internal"], ["unittest"])
        problem = "Should we use tabs or spaces?"
        decision = agent.process(problem)
        self.assertEqual(decision, "HemiA_decide")
        self.assertEqual(len(agent.decision_logs), 1)
        self.assertEqual(agent.decision_logs[0]["problem"], problem)

    def test_arbitration_logic(self):
        hemi_c = HemisphereC()
        # Test case 1: Hemisphere A has higher confidence
        decision_a = {"decision": "A", "confidence": 0.9}
        decision_b = {"decision": "B", "confidence": 0.8}
        self.assertEqual(hemi_c.arbitrate(decision_a, decision_b), "A")

        # Test case 2: Hemisphere B has higher confidence
        decision_a = {"decision": "A", "confidence": 0.8}
        decision_b = {"decision": "B", "confidence": 0.9}
        self.assertEqual(hemi_c.arbitrate(decision_a, decision_b), "B")

        # Test case 3: Equal confidence
        decision_a = {"decision": "A", "confidence": 0.9}
        decision_b = {"decision": "B", "confidence": 0.9}
        self.assertEqual(hemi_c.arbitrate(decision_a, decision_b), "A")

if __name__ == '__main__':
    unittest.main()