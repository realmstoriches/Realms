import unittest
import os
from unittest.mock import patch
from src.payments import create_stripe_product, create_payment_link

class TestPayments(unittest.TestCase):

    @patch.dict(os.environ, {"STRIPE_API_KEY": "test_key"})
    def test_create_stripe_product(self):
        product_id = create_stripe_product("Test Product")
        self.assertIsNotNone(product_id)
        self.assertTrue(product_id.startswith("prod_"))

    @patch.dict(os.environ, {"STRIPE_API_KEY": "test_key"})
    def test_create_payment_link(self):
        payment_link = create_payment_link("prod_test")
        self.assertIsNotNone(payment_link)
        self.assertTrue(payment_link.startswith("https://buy.stripe.com/"))

    def test_no_api_key(self):
        # Ensure functions handle missing API key gracefully
        with patch.dict(os.environ, {}, clear=True):
            product_id = create_stripe_product("Test Product")
            self.assertIsNone(product_id)
            payment_link = create_payment_link("prod_test")
            self.assertIsNone(payment_link)

if __name__ == '__main__':
    unittest.main()