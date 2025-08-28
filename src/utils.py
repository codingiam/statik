import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                nodes.append(TextNode(parts[i], text_type))
    return nodes

def extract_markdown_images(text, iter = False):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    if not iter:
        return re.findall(pattern, text)
    else:
        return list(re.finditer(pattern, text))

def extract_markdown_links(text, iter = False):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    if not iter:
        return re.findall(pattern, text)
    else:
        return list(re.finditer(pattern, text))

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text, iter=True)
        if images:
            last_end = 0
            for match in images:
                start, end = match.span()
                if start > last_end:
                    nodes.append(TextNode(text[last_end:start], TextType.TEXT))
                link_text, href = match.groups()
                nodes.append(TextNode(link_text, TextType.IMAGE, href))
                last_end = end
            if last_end < len(text):
                nodes.append(TextNode(text[last_end:], TextType.TEXT))
        else:
            nodes.append(node)

    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text, iter=True)
        if links:
            last_end = 0
            for match in links:
                start, end = match.span()
                if start > last_end:
                    nodes.append(TextNode(text[last_end:start], TextType.TEXT))
                link_text, href = match.groups()
                nodes.append(TextNode(link_text, TextType.LINK, href))
                last_end = end
            if last_end < len(text):
                nodes.append(TextNode(text[last_end:], TextType.TEXT))
        else:
            nodes.append(node)

    return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
