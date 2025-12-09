class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

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
