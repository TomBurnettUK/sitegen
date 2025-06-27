import unittest

from convert import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    text_node_to_html_node,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://img.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://img.com/img.png", "alt": "Alt text"}
        )

    def test_invalid_type(self):
        class DummyType:
            pass

        node = TextNode("Invalid", DummyType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestTextToTextNodes(unittest.TestCase):
    def test_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertEqual(
            textnodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_no_formatting(self):
        text = "Just plain text."
        textnodes = text_to_textnodes(text)
        self.assertEqual(textnodes, [TextNode("Just plain text.", TextType.TEXT)])

    def test_multiple_images_and_links(self):
        text = "![img1](url1) and [link1](url2) and ![img2](url3)"
        textnodes = text_to_textnodes(text)
        self.assertEqual(
            textnodes,
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url2"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url3"),
            ],
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_only_whitespace(self):
        md = "   \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_single_block(self):
        md = "Just a single block with no double newlines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block with no double newlines."])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading 1"),
            BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type("### Heading 3"),
            BlockType.HEADING,
        )

    def test_code_block(self):
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(code_block),
            BlockType.CODE,
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> This is a quote"),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2"),
            BlockType.UNORDERED_LIST,
        )
        self.assertNotEqual(
            block_to_block_type("-item 1\n-item 2"),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. item 1\n2. item 2"),
            BlockType.ORDERED_LIST,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."),
            BlockType.PARAGRAPH,
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def xtest_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def xtest_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
