from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, object] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        html = []
        for child in self.children:
            html.append(child.to_html())
        return f"<{self.tag}>{"".join(html)}</{self.tag}>"