import unittest
import random
from src.agent import Agent
from src.knowledge import KnowledgeBase
from src.testing import evaluate_product
from src.company import generate_employee_file, ORG_CHART

class TestTesting(unittest.TestCase):

    def setUp(self):
        self.kb = KnowledgeBase(collection_name=f"test_testing_{random.randint(1000, 9999)}")
        self.product_data = {
            "product_name": "Test Product",
            "evaluation_questions": {
                "AI Infrastructure Engineer": "Q1",
                "Research Scientist": "Q2"
            }
        }

        ai_role = next(r for d in ORG_CHART.values() for r in d if r['title'] == 'AI Infrastructure Engineer')
        rs_role = next(r for d in ORG_CHART.values() for r in d if r['title'] == 'Research Scientist')

        ai_agent_data = generate_employee_file(ai_role)
        rs_agent_data = generate_employee_file(rs_role)

        self.crew = [
            Agent(
                name=ai_agent_data['name'],
                role=ai_agent_data['role_title'],
                employee_id=ai_agent_data['employee_id'],
                hourly_rate=ai_agent_data['hourly_rate'],
                physical_description=ai_agent_data['physical_description'],
                skill_matrix=ai_agent_data['skill_matrix'],
                knowledge_sources=ai_agent_data['knowledge_sources'],
                tool_access=ai_agent_data['tool_access'],
                knowledge_base=self.kb
            ),
            Agent(
                name=rs_agent_data['name'],
                role=rs_agent_data['role_title'],
                employee_id=rs_agent_data['employee_id'],
                hourly_rate=rs_agent_data['hourly_rate'],
                physical_description=rs_agent_data['physical_description'],
                skill_matrix=rs_agent_data['skill_matrix'],
                knowledge_sources=rs_agent_data['knowledge_sources'],
                tool_access=rs_agent_data['tool_access'],
                knowledge_base=self.kb
            )
        ]

    def test_evaluate_product(self):
        feedback = evaluate_product(self.crew, self.product_data)

        self.assertEqual(len(feedback), 2)

        ai_agent_name = self.crew[0].name
        self.assertIn(ai_agent_name, feedback)
        self.assertEqual(feedback[ai_agent_name]['role'], 'AI Infrastructure Engineer')
        self.assertEqual(feedback[ai_agent_name]['question'], 'Q1')

        rs_agent_name = self.crew[1].name
        self.assertIn(rs_agent_name, feedback)
        self.assertEqual(feedback[rs_agent_name]['role'], 'Research Scientist')
        self.assertEqual(feedback[rs_agent_name]['question'], 'Q2')

if __name__ == '__main__':
    unittest.main()