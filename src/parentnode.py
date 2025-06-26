from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None or self.children == []:
            raise ValueError("Parent node must have children")

        outputHTML = ""
        for node in self.children:
            outputHTML += f"<{self.tag}>{node.to_html()}</{self.tag}>"

        return outputHTML
