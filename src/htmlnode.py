class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        complete = []
        if self.props is None or self.props == "":
            return ""
        for key, value in self.props.items():
            complete.append(f' {key}="{value}"')
        return "".join(complete)


    def __eq__(self, other):
        if type(other) is not HTMLNode:
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
#        if self.value is None:
#            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        if self.tag == 'img':
            print(f"<{self.tag}{self.props_to_html()}>")
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.tag}, {self.value}, {self.props})"    


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("ParentNode must have children.")
        results = ""
        for child in self.children:
            results += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{results}</{self.tag}>"

    def __repr__(self):
        return f"{type(self).__name__}({self.tag}, {self.children}, {self.props})"

    # # Official
    # class ParentNode(HTMLNode):
    # def __init__(self, tag, children, props=None):
    #     super().__init__(tag, None, children, props)

    # def to_html(self):
    #     if self.tag is None:
    #         raise ValueError("invalid HTML: no tag")
    #     if self.children is None:
    #         raise ValueError("invalid HTML: no children")
    #     children_html = ""
    #     for child in self.children:
    #         children_html += child.to_html()
    #     return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    # def __repr__(self):
    #     return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
