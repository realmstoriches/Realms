import unittest
import os
from unittest.mock import patch
from src.social import twitter, facebook

class TestSocial(unittest.TestCase):

    @patch.dict(os.environ, {"TWITTER_API_KEY": "test", "TWITTER_API_SECRET": "test"})
    def test_twitter_authenticate(self):
        self.assertTrue(twitter.authenticate())

    @patch.dict(os.environ, {"TWITTER_API_KEY": "test", "TWITTER_API_SECRET": "test"})
    def test_twitter_post(self):
        result = twitter.post_update("Hello")
        self.assertEqual(result["platform"], "Twitter")

    @patch.dict(os.environ, {"FACEBOOK_APP_ID": "test", "FACEBOOK_APP_SECRET": "test"})
    def test_facebook_authenticate(self):
        self.assertTrue(facebook.authenticate())

    @patch.dict(os.environ, {"FACEBOOK_APP_ID": "test", "FACEBOOK_APP_SECRET": "test"})
    def test_facebook_post(self):
        result = facebook.post_update("Hello")
        self.assertEqual(result["platform"], "Facebook")

if __name__ == '__main__':
    unittest.main()