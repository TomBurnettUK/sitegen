import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_with_whitespace(self):
        self.assertEqual(extract_title("   #   Hello World   "), "Hello World")

    def test_multiline(self):
        md = """
Some intro text
# My Title
Some more text
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_no_h1(self):
        md = """
## Subtitle
Some text
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_h1_not_first_line(self):
        md = """
Text before
# Title Here
"""
        self.assertEqual(extract_title(md), "Title Here")


if __name__ == "__main__":
    unittest.main()
