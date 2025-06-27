from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        props_html = ""
        if self.props:
            props_html = " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())
        if self.tag == "img":
            return f"<img{props_html}/>"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
