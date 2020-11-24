import matplotlib.pyplot as plt
import networkx as nx
from TreePrinter import indent_representation
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

def parse_line_to_indent_token(line: str, indent_text: str = indent_representation) -> (int, str):
    indent = line.count(indent_text)
    return (indent, line[indent * len(indent_text):])

def dfs(tree_text: str) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_node(0, token='START')
    parents = [0]
    index = 1
    find_my_index = lambda indent: indent+1
    for line in tree_text.splitlines():
        indent, token = parse_line_to_indent_token(line)
        token_indent_index = find_my_index(indent)
        if token_indent_index > len(parents) - 1:
            parents += [index]
        G.add_node(index, token=token)
        G.add_edge(parents[token_indent_index-1], index)
        parents[token_indent_index] = index
        index += 1
    return G

def draw_tree_from_text(text, filename = None):
    plt.figure(figsize=(30,40))
    G = dfs(text)
    
    pos = graphviz_layout(G, prog='dot')
        
    labels = {u: d for u,d in G.nodes(data='token')} 
    
    nx.draw_networkx(
        G, 
        pos, 
        arrows=True,
        labels=labels,
        node_size = 500,
        node_color = "#f1f1f1",
        font_size = 10
    )
    
    if filename:
        plt.savefig(filename)
    else:
        plt.show()