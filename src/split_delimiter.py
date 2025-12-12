from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            flag = False
            loopnodes = old_node.text.split(delimiter)
            if len(loopnodes) % 2 == 0:
                print("something is wrong here")
            for node in loopnodes:
                if node == "":
                    flag = True
                    continue
                elif flag:
                    new_nodes.append(TextNode(node, text_type))
                    flag = False
                else:
                    new_nodes.append(TextNode(node, TextType.TEXT))
                    flag = True
    return new_nodes
