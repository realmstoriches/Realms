import unittest
import random
from src.agent import Agent, HemisphereA, HemisphereB, HemisphereC
from src.knowledge import KnowledgeBase

class TestAgent(unittest.TestCase):

    def setUp(self):
        # Create a unique knowledge base for each test to ensure isolation
        self.kb = KnowledgeBase(collection_name=f"test_agent_{random.randint(1000, 9999)}")
        self.agent = Agent(
            name="Test Agent",
            role="Tester",
            employee_id="12345",
            hourly_rate=50.0,
            physical_description="A test agent.",
            skill_matrix=["testing"],
            knowledge_sources=["internal"],
            tool_access=["unittest"],
            knowledge_base=self.kb
        )

    def test_agent_creation(self):
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertIsInstance(self.agent.hemisphere_a, HemisphereA)
        self.assertIsInstance(self.agent.hemisphere_b, HemisphereB)
        self.assertIsInstance(self.agent.hemisphere_c, HemisphereC)
        self.assertIs(self.agent.knowledge_base, self.kb)

    def test_decision_process_with_knowledge(self):
        problem = "Should we use tabs or spaces?"
        knowledge = "The best practice is to use spaces for indentation."
        self.kb.add_document(knowledge, {"source": "style_guide"}, "doc1")

        decision = self.agent.process(problem)
        expected_decision = f"HemiA decides based on: {knowledge}"
        self.assertEqual(decision, expected_decision)
        self.assertEqual(len(self.agent.decision_logs), 1)
        self.assertEqual(self.agent.decision_logs[0]["problem"], problem)

    def test_decision_process_no_knowledge(self):
        problem = "What is the meaning of life?"
        decision = self.agent.process(problem)
        self.assertEqual(decision, "HemiA_decide_no_knowledge")

    def test_advanced_arbitration_logic(self):
        hemi_c_A = HemisphereC(fallback_heuristic='A')
        decision_a = {"decision": "A", "confidence": 0.9}
        decision_b = {"decision": "B", "confidence": 0.8}

        # Test case 1: Hemisphere A has higher confidence
        self.assertEqual(hemi_c_A.arbitrate(decision_a, decision_b), "A")

        # Test case 2: Hemisphere B has higher confidence
        decision_b_strong = {"decision": "B_strong", "confidence": 0.95}
        self.assertEqual(hemi_c_A.arbitrate(decision_a, decision_b_strong), "B_strong")

        # Test case 3: Equal confidence with fallback to A
        decision_c = {"decision": "C", "confidence": 0.9}
        self.assertEqual(hemi_c_A.arbitrate(decision_a, decision_c), "A")

        # Test case 4: Equal confidence with fallback to B
        hemi_c_B = HemisphereC(fallback_heuristic='B')
        self.assertEqual(hemi_c_B.arbitrate(decision_a, decision_c), "C")

        # Test case 5: Weighted scoring favoring B
        weights = {'A': 0.8, 'B': 1.0}
        decision_d = {"decision": "D", "confidence": 0.9} # score = 0.72
        decision_e = {"decision": "E", "confidence": 0.8} # score = 0.8
        self.assertEqual(hemi_c_A.arbitrate(decision_d, decision_e, weights), "E")

if __name__ == '__main__':
    unittest.main()