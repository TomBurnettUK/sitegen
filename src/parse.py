import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError(f"Closing delimeter {delimiter} not found")
            for i in range(len(split_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue

        last_index = 0
        for alt, link in images:
            img_text = f"![{alt}]({link})"
            idx = text.find(img_text, last_index)
            if idx > last_index:
                new_nodes.append(TextNode(text[last_index:idx], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            last_index = idx + len(img_text)
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue

        last_index = 0
        for alt, link in links:
            link_text = f"[{alt}]({link})"
            idx = text.find(link_text, last_index)
            if idx > last_index:
                new_nodes.append(TextNode(text[last_index:idx], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            last_index = idx + len(link_text)
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
