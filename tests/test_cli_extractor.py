import unittest

import cli


class ExtractorTests(unittest.TestCase):
    def test_extracts_disaster_schema(self):
        record = cli.extract_record(
            "SOS: 52 people near Lake Road School need drinking water, food, blankets "
            "and medical help. Contact +91 90000 11111.",
            "sample.txt",
        )

        self.assertEqual(record["urgency"], "critical")
        self.assertEqual(record["peopleAffected"], 52)
        self.assertIn("water", record["needs"])
        self.assertIn("food", record["needs"])
        self.assertTrue(record["contact"]["phone"])
        self.assertGreaterEqual(record["confidence"], 80)


if __name__ == "__main__":
    unittest.main()
