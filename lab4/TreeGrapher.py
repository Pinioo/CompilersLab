import matplotlib.pyplot as plt
from TreePrinter import indent_representation
from graphviz import Digraph

def parse_line_to_indent_token(line: str, indent_text: str = indent_representation) -> (int, str):
    indent = line.count(indent_text)
    return (indent, line[indent * len(indent_text):])

def dfs(tree_text: str) -> Digraph:
    G = Digraph()
    G.node('0', label='START')
    parents = [0]
    index = 1
    find_my_index = lambda indent: indent+1
    for line in tree_text.splitlines():
        indent, token = parse_line_to_indent_token(line)
        token_indent_index = find_my_index(indent)
        if token_indent_index > len(parents) - 1:
            parents += [index]
        G.node(f'{index}', label=token)
        G.edge(f'{parents[token_indent_index-1]}', f'{index}')
        parents[token_indent_index] = index
        index += 1
    return G

def draw_tree_from_text(text, filename='graph'):
    G = dfs(text)
    G.render(filename, view=True)