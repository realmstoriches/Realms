import unittest
import os
import json
import tempfile
from src.arrangements import generate_manifest, ARRANGEMENT_TEMPLATES

class TestArrangements(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_manifest(self):
        arrangement_name = "Development"
        template = ARRANGEMENT_TEMPLATES[arrangement_name]
        manifest_path = generate_manifest(arrangement_name, template, self.output_dir)

        self.assertTrue(os.path.exists(manifest_path))

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        self.assertEqual(manifest["arrangement_name"], arrangement_name)
        self.assertEqual(manifest["optimization_focus"], template["optimization_focus"])
        self.assertEqual(len(manifest["agent_roster"]), len(template["roles"]))

if __name__ == '__main__':
    unittest.main()