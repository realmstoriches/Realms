import unittest
from src.company import generate_employee_file, ORG_CHART

class TestCompany(unittest.TestCase):

    def test_generate_employee_file(self):
        role_def = ORG_CHART["Software"][0] # AI Infrastructure Engineer
        employee_file = generate_employee_file(role_def)

        self.assertIn("name", employee_file)
        self.assertEqual(employee_file["role_title"], "AI Infrastructure Engineer")
        self.assertIn("employee_id", employee_file)
        self.assertIsInstance(employee_file["hourly_rate"], float)
        self.assertEqual(employee_file["skill_matrix"], ["Python", "Kubernetes", "Docker", "TensorFlow", "PyTorch"])
        self.assertEqual(employee_file["knowledge_sources"], ["Software"])
        self.assertEqual(employee_file["tool_access"], ["Jenkins", "Git", "Jira"])

if __name__ == '__main__':
    unittest.main()