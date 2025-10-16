import unittest
from unittest.mock import MagicMock
from src.business_logic import generate_founders_packet

class TestBusinessLogic(unittest.TestCase):

    def test_generate_founders_packet(self):
        # Create mock agents
        cfo = MagicMock()
        legal = MagicMock()
        strategist = MagicMock()
        analyst = MagicMock()

        # Define the return values for the mock agents' process method
        cfo.process.return_value = "Financials"
        legal.process.return_value = "Legal Doc"
        strategist.process.return_value = "Pitch Deck"
        analyst.process.return_value = "Audience"

        packet = generate_founders_packet(cfo, legal, strategist, analyst)

        self.assertEqual(packet["financial_projections"], "Financials")
        self.assertEqual(packet["founders_agreement_template"], "Legal Doc")
        self.assertEqual(packet["pitch_deck_outline"], "Pitch Deck")
        self.assertEqual(packet["audience_profiles"], "Audience")

if __name__ == '__main__':
    unittest.main()