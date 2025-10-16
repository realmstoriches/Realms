import unittest
import json
from app.main import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_live_data_endpoint(self):
        # Create a dummy live_data.json to be served
        dummy_data = {"status": "testing", "current_phase": "Test", "recent_events": []}
        with open("live_data.json", "w") as f:
            json.dump(dummy_data, f)

        response = self.app.get('/api/live_data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "testing")

    def test_oauth_login_placeholder(self):
        response = self.app.get('/auth/twitter/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'redirect you to twitter', response.data)

if __name__ == '__main__':
    unittest.main()