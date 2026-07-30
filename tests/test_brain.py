import unittest
from caelis.intelligence.brain import Brain
from caelis.language.detector import detect_language
from caelis.intelligence.local_ai import LocalAI


class TestSpeedAndAccuracy(unittest.TestCase):

    def setUp(self):
        self.brain = Brain()

    def test_phonetic_variations_and_punctuation(self):
        # Test "Vanakkam, empadi iruka." with comma and period
        resp1 = self.brain.process("Vanakkam, empadi iruka.", language="thanglish")
        self.assertIn("super-ah iruken", resp1)

        # Test "Nuna lana, panra, mudiyum." (Whisper STT output for unnala enna panna mudiyum)
        resp2 = self.brain.process("Nuna lana, panra, mudiyum.", language="thanglish")
        self.assertIn("panna mudiyum", resp2)

        # Test language detection for phonetic variations
        self.assertEqual(detect_language("empadi iruka"), "thanglish")
        self.assertEqual(detect_language("Nuna lana, panra, mudiyum."), "thanglish")

    def test_bracket_stripping(self):
        cleaned = LocalAI._clean_speech_text("[Nalla] Vanakkam BS, naan thavaraiku irukeenga! *Nee* epdi irukeenga?")
        self.assertNotIn("[Nalla]", cleaned)
        self.assertNotIn("*", cleaned)
        self.assertTrue(cleaned.startswith("Vanakkam BS"))


if __name__ == "__main__":
    unittest.main()
