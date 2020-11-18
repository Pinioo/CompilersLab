import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

def dfs(node, G, index = 0):
    node.index = index
    if node.parent is not None:
        G.add_edge(node.parent.index, index, L=node.letter)
    index += 1
    for v in node.children.values():
        index = dfs(v, G, index)
    return index

def draw_trie(root, filename = None):
    plt.figure(figsize=(30,40))
    G = nx.DiGraph()
    dfs(root, G)
    
    pos = graphviz_layout(G, prog='dot')
        
    edge_labels = {(u,v): d['L'] for u,v,d in G.edges(data=True)} 
    
    nx.draw_networkx_edges(G, pos, arrows=True)   
    nx.draw_networkx_edge_labels(G, pos, font_size=30, edge_labels=edge_labels)
    
    if filename:
        plt.savefig(filename)
    else:
        plt.show()