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

    def test_decision_process_with_knowledge(self):
        agent = Agent("Test Agent", "Tester", "12345", 50.0, "A test agent.", ["testing"], ["internal"], ["unittest"])

        # Add a document to the agent's knowledge base
        problem = "Should we use tabs or spaces?"
        knowledge = "The best practice is to use spaces for indentation."
        agent.knowledge_base.add_document(knowledge, {"source": "style_guide"}, "doc1")

        decision = agent.process(problem)
        expected_decision = f"HemiA decides based on: {knowledge}"
        self.assertEqual(decision, expected_decision)
        self.assertEqual(len(agent.decision_logs), 1)
        self.assertEqual(agent.decision_logs[0]["problem"], problem)

    def test_decision_process_no_knowledge(self):
        agent = Agent("Test Agent", "Tester", "12345", 50.0, "A test agent.", ["testing"], ["internal"], ["unittest"])
        problem = "What is the meaning of life?"
        decision = agent.process(problem)
        self.assertEqual(decision, "HemiA_decide_no_knowledge")

    def test_advanced_arbitration_logic(self):
        # Test case 1: Hemisphere A has higher confidence
        hemi_c_A = HemisphereC(fallback_heuristic='A')
        decision_a = {"decision": "A", "confidence": 0.9}
        decision_b = {"decision": "B", "confidence": 0.8}
        self.assertEqual(hemi_c_A.arbitrate(decision_a, decision_b), "A")

        # Test case 2: Hemisphere B has higher confidence
        self.assertEqual(hemi_c_A.arbitrate(decision_b, decision_a), "A")

        # Test case 3: Equal confidence with fallback to A
        decision_c = {"decision": "C", "confidence": 0.9}
        self.assertEqual(hemi_c_A.arbitrate(decision_a, decision_c), "A")

        # Test case 4: Equal confidence with fallback to B
        hemi_c_B = HemisphereC(fallback_heuristic='B')
        self.assertEqual(hemi_c_B.arbitrate(decision_a, decision_c), "C")

        # Test case 5: Weighted scoring favoring B
        weights = {'A': 0.8, 'B': 1.0}
        decision_d = {"decision": "D", "confidence": 0.9}
        decision_e = {"decision": "E", "confidence": 0.8}
        self.assertAlmostEqual(0.9 * 0.8, 0.72)
        self.assertEqual(hemi_c_A.arbitrate(decision_d, decision_e, weights), "E")

if __name__ == '__main__':
    unittest.main()