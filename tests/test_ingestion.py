import unittest
import os
import tempfile
import random
from src.ingestion import ingest_text_file
from src.knowledge import KnowledgeBase

class TestIngestion(unittest.TestCase):

    def setUp(self):
        # Create a unique knowledge base for each test to ensure isolation
        self.knowledge_base = KnowledgeBase(collection_name=f"test_ingestion_{random.randint(1000, 9999)}")

        # Create a temporary file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_ingestion_data.txt")

        with open(self.test_file, "w") as f:
            f.write("Test knowledge 1\n")
            f.write("Test knowledge 2\n")

    def tearDown(self):
        # Clean up the temporary directory and file
        self.temp_dir.cleanup()

    def test_ingest_text_file(self):
        ingest_text_file(self.knowledge_base, self.test_file)
        results = self.knowledge_base.collection.get()
        self.assertEqual(len(results['documents']), 2)
        self.assertIn("Test knowledge 1", results['documents'])
        self.assertIn("Test knowledge 2", results['documents'])

if __name__ == '__main__':
    unittest.main()