import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")

    def test_repr_with_tag_value(self):
        node = HTMLNode("tag", "value")
        self.assertEqual(str(node), "HTMLNode(tag, value, None, None)")

    def test_repr_with_children(self):
        node = HTMLNode("tag", "value", [])
        self.assertEqual(str(node), "HTMLNode(tag, value, [], None)")

    def test_repr_with_props(self):
        node = HTMLNode("tag", "value", props={})
        self.assertEqual(str(node), "HTMLNode(tag, value, None, {})")


if __name__ == "__main__":
    unittest.main()
