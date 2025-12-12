import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
    
def markdown_to_blocks(text):
    final_list = []
    candidates_list = text.split("\n\n")
    print(candidates_list)
    for candidate in candidates_list:
        if candidate == "":
            continue
        else:
            final_list.append(candidate.strip())
    return final_list

def block_to_block_type(text):
    heading = re.compile(r'#{1,6} .*')
    code = re.compile(r'^```.*```$')
    if heading.search(text):
        return BlockType.HEADING
    if code.search(text):
        return BlockType.CODE
    is_quote = True
    is_unordered = True
    is_ordered = True
    count_ordered = 1
    line_list = text.split("\n")
    for line in line_list:
        if line == "":
            continue
        if not line.startswith('>'):
            is_quote = False
        if not line.startswith('-'):
            is_unordered = False
        if not line.startswith(str(count_ordered) + '.' + ' '):
            is_ordered = False
        count_ordered += 1
    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

    
text = "###### This is a headline"
heading = block_to_block_type(text)
print(heading)

text2 = "```print(some_variable)```"
code = block_to_block_type(text2)
print(code)

text3 = "- First unordered_list"
ordered = block_to_block_type(text3)
print(ordered)

text4 = """
1. first point
2. second point
3. a very good point
4. final point
"""
ordered2 = block_to_block_type(text4)
print(ordered2)
