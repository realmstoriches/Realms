import unittest
import os
import json
import tempfile
from src.live_data_utils import update_live_data, set_live_data_status, LIVE_DATA_FILE

class TestLiveData(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir.name)
        # Ensure no old file exists
        if os.path.exists(LIVE_DATA_FILE):
            os.remove(LIVE_DATA_FILE)

    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def test_update_live_data(self):
        update_live_data("Test Phase", "Test Agent", "Test Action")

        self.assertTrue(os.path.exists(LIVE_DATA_FILE))
        with open(LIVE_DATA_FILE, 'r') as f:
            data = json.load(f)

        self.assertEqual(data["status"], "running")
        self.assertEqual(data["current_phase"], "Test Phase")
        self.assertEqual(len(data["recent_events"]), 1)
        self.assertEqual(data["recent_events"][0]["agent"], "Test Agent")
        self.assertEqual(data["recent_events"][0]["action"], "Test Action")

    def test_set_live_data_status(self):
        set_live_data_status("complete")

        self.assertTrue(os.path.exists(LIVE_DATA_FILE))
        with open(LIVE_DATA_FILE, 'r') as f:
            data = json.load(f)

        self.assertEqual(data["status"], "complete")

if __name__ == '__main__':
    unittest.main()