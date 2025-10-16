import unittest
from src.knowledge import KnowledgeBase

class TestKnowledgeBase(unittest.TestCase):

    def test_add_and_query(self):
        kb = KnowledgeBase(collection_name="test_kb")
        kb.add_document("Test document", {"source": "test"}, "doc1")
        results = kb.query("Test")
        self.assertEqual(len(results['documents'][0]), 1)
        self.assertEqual(results['documents'][0][0], "Test document")

if __name__ == '__main__':
    unittest.main()