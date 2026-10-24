import os
import tempfile
import unittest

import casl_check

GOOD = """Hi Sam,

Short note about the meetup next week.

Alex Example, Example Widgets Inc.
100 Sample St, Unit 5, Toronto, ON M5V 1A1 · example.com
Reply "unsubscribe" and we won't write again.
"""


class DraftTests(unittest.TestCase):
    def test_complete_footer(self):
        self.assertEqual(casl_check.check_draft(GOOD, "Alex Example"), [])

    def test_missing_everything(self):
        missing = casl_check.check_draft("Hi Sam, quick note.")
        self.assertEqual(len(missing), 3)

    def test_missing_unsubscribe_only(self):
        missing = casl_check.check_draft(GOOD.replace('Reply "unsubscribe" and we won\'t write again.', ""))
        self.assertEqual(len(missing), 1)
        self.assertIn("unsubscribe", missing[0])

    def test_french_unsubscribe(self):
        text = GOOD.replace('Reply "unsubscribe"', "Pour vous désabonner, répondez")
        self.assertEqual(casl_check.check_draft(text), [])


class SuppressionTests(unittest.TestCase):
    def test_header_and_case(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "s.csv")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("Name,Email Address,Date\nA,Blocked@Example.com,2026-01-01\n")
            suppressed = casl_check.load_suppression(path)
            self.assertEqual(casl_check.check_recipients(["blocked@example.com", "ok@example.com"], suppressed),
                             ["blocked@example.com"])


if __name__ == "__main__":
    unittest.main()
