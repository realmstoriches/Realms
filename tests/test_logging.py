import unittest
import os
import tempfile
from src.logging import log_post_performance

class TestLogging(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        # Override the default log directory for testing
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def test_log_post_performance(self):
        log_file = "logs/social_media_performance.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        log_post_performance("Test Product", "twitter", success=True)
        self.assertTrue(os.path.exists(log_file))

        with open(log_file, "r") as f:
            content = f.read()
            self.assertIn("Test Product", content)
            self.assertIn("twitter", content)
            self.assertIn("SUCCESS", content)

if __name__ == '__main__':
    unittest.main()