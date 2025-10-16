import unittest
import os
from unittest.mock import patch
from src.social import twitter, facebook, linkedin, wordpress, instagram, reddit

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

    @patch.dict(os.environ, {"LINKEDIN_CLIENT_ID": "test", "LINKEDIN_CLIENT_SECRET": "test"})
    def test_linkedin_post(self):
        result = linkedin.post_update("Hello")
        self.assertEqual(result["platform"], "LinkedIn")

    @patch.dict(os.environ, {"WORDPRESS_USER": "test", "WORDPRESS_PASSWORD": "test"})
    def test_wordpress_post(self):
        result = wordpress.post_update("Hello")
        self.assertEqual(result["platform"], "WordPress")

    @patch.dict(os.environ, {"INSTAGRAM_USERNAME": "test", "INSTAGRAM_PASSWORD": "test"})
    def test_instagram_post(self):
        result = instagram.post_update("Hello")
        self.assertEqual(result["platform"], "Instagram")

    @patch.dict(os.environ, {"REDDIT_CLIENT_ID": "test", "REDDIT_CLIENT_SECRET": "test", "REDDIT_USERNAME": "test", "REDDIT_PASSWORD": "test"})
    def test_reddit_post(self):
        result = reddit.post_update("Hello", subreddit="test")
        self.assertEqual(result["platform"], "Reddit")

if __name__ == '__main__':
    unittest.main()