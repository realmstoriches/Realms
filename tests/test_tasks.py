import unittest
import random
import os
from unittest.mock import patch
from src.agent import Agent
from src.knowledge import KnowledgeBase
from src.tasks import evaluate_product, generate_marketing_content, post_in_parallel, design_marketing_campaign
from src.company import generate_employee_file, ORG_CHART

class TestTasks(unittest.TestCase):

    def setUp(self):
        self.kb = KnowledgeBase(collection_name=f"test_testing_{random.randint(1000, 9999)}")
        self.product_data = {
            "product_name": "Test Product",
            "evaluation_questions": {
                "AI Infrastructure Engineer": "Q1",
                "Research Scientist": "Q2"
            }
        }

        # Create deterministic agent data for testing to avoid random name collisions
        ai_agent_data = {
            "name": "Test AI Engineer", "role_title": "AI Infrastructure Engineer", "employee_id": "1",
            "hourly_rate": 100.0, "physical_description": "", "skill_matrix": [],
            "knowledge_sources": [], "tool_access": []
        }
        rs_agent_data = {
            "name": "Test Research Scientist", "role_title": "Research Scientist", "employee_id": "2",
            "hourly_rate": 100.0, "physical_description": "", "skill_matrix": [],
            "knowledge_sources": [], "tool_access": []
        }

        self.crew = [
            Agent(
                name=ai_agent_data['name'], role=ai_agent_data['role_title'],
                employee_id=ai_agent_data['employee_id'], hourly_rate=ai_agent_data['hourly_rate'],
                physical_description=ai_agent_data['physical_description'], skill_matrix=ai_agent_data['skill_matrix'],
                knowledge_sources=ai_agent_data['knowledge_sources'], tool_access=ai_agent_data['tool_access'],
                knowledge_base=self.kb
            ),
            Agent(
                name=rs_agent_data['name'], role=rs_agent_data['role_title'],
                employee_id=rs_agent_data['employee_id'], hourly_rate=rs_agent_data['hourly_rate'],
                physical_description=rs_agent_data['physical_description'], skill_matrix=rs_agent_data['skill_matrix'],
                knowledge_sources=rs_agent_data['knowledge_sources'], tool_access=rs_agent_data['tool_access'],
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

    def test_generate_marketing_content(self):
        marketing_role = next(r for d in ORG_CHART.values() for r in d if r['title'] == 'Marketing Content Creator')
        marketing_agent_data = generate_employee_file(marketing_role)
        marketing_agent = Agent(
            name=marketing_agent_data['name'],
            role=marketing_agent_data['role_title'],
            employee_id=marketing_agent_data['employee_id'],
            hourly_rate=marketing_agent_data['hourly_rate'],
            physical_description=marketing_agent_data['physical_description'],
            skill_matrix=marketing_agent_data['skill_matrix'],
            knowledge_sources=marketing_agent_data['knowledge_sources'],
            tool_access=marketing_agent_data['tool_access'],
            knowledge_base=self.kb
        )

        product_data = {
            "product_name": "Test Product",
            "variants": [{"options": {"Feature": "Value"}}]
        }
        content = generate_marketing_content(marketing_agent, product_data)

        self.assertIn("tweet", content)
        self.assertIn("facebook_post", content)
        self.assertIsInstance(content["tweet"], str)
        self.assertIsInstance(content["facebook_post"], str)

    @patch.dict(os.environ, {"TWITTER_API_KEY": "test", "FACEBOOK_APP_ID": "test", "TWITTER_API_SECRET": "test", "FACEBOOK_APP_SECRET": "test"})
    def test_post_in_parallel(self):
        content = {
            "twitter": "Test tweet",
            "facebook": "Test facebook post"
        }
        results = post_in_parallel(content, "Test Product")
        self.assertEqual(len(results), 2)
        platforms = {r['platform'] for r in results}
        self.assertIn("Twitter", platforms)
        self.assertIn("Facebook", platforms)

    def test_design_marketing_campaign(self):
        strategist_role = next(r for d in ORG_CHART.values() for r in d if r['title'] == 'Campaign Strategist')
        strategist_data = generate_employee_file(strategist_role)
        strategist = Agent(
            name=strategist_data['name'],
            role=strategist_data['role_title'],
            employee_id=strategist_data['employee_id'],
            hourly_rate=strategist_data['hourly_rate'],
            physical_description=strategist_data['physical_description'],
            skill_matrix=strategist_data['skill_matrix'],
            knowledge_sources=strategist_data['knowledge_sources'],
            tool_access=strategist_data['tool_access'],
            knowledge_base=self.kb
        )

        product_data = {"product_name": "Test Campaign Product"}
        campaign = design_marketing_campaign(strategist, product_data)

        self.assertEqual(campaign["product_name"], "Test Campaign Product")
        self.assertIn("campaign_plan", campaign)
        self.assertIsInstance(campaign["campaign_plan"], str)


if __name__ == '__main__':
    unittest.main()