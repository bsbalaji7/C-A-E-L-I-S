import unittest
from caelis.language.detector import detect_language


class TestLanguageDetector(unittest.TestCase):

    def test_english_detection(self):
        self.assertEqual(detect_language("Hello CAELIS"), "english")
        self.assertEqual(detect_language("What is the time right now?"), "english")
        self.assertEqual(detect_language("Open Google Chrome"), "english")
        self.assertEqual(detect_language("Who are you?"), "english")

    def test_thanglish_detection(self):
        self.assertEqual(detect_language("vanakkam caelis"), "thanglish")
        self.assertEqual(detect_language("epdi iruka"), "thanglish")
        self.assertEqual(detect_language("eppadi irukeenga"), "thanglish")
        self.assertEqual(detect_language("unnala enna panna mudiyum"), "thanglish")
        self.assertEqual(detect_language("inniku date enna"), "thanglish")
        self.assertEqual(detect_language("ippo time enna"), "thanglish")
        self.assertEqual(detect_language("nalla iruken bro"), "thanglish")
        self.assertEqual(detect_language("solunga"), "thanglish")

    def test_tamil_script_detection(self):
        self.assertEqual(detect_language("வணக்கம்"), "tamil")
        self.assertEqual(detect_language("எப்படி இருக்கீங்க"), "tamil")


if __name__ == "__main__":
    unittest.main()
