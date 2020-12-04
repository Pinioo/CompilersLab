# To run draw_tree_from_text, install:
# - graphviz package (pip install graphviz)
# - graphviz (https://graphviz.org/) (not necessary, required to draw the graph)

import sys
import scanner
import Mparser
from TreePrinter import TreePrinter
from TreeGrapher import draw_tree_from_text
from TypeChecker import TypeChecker


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    
    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer, tracking=True)
    
    tree_text = ast.printTree()
    # print(tree_text)
    # draw_tree_from_text(tree_text, 'graph')

    tc = TypeChecker()
    tc.visit(ast)
    if tc.error_counter == 0:
        print("No errors found")
    else:
        print(f"! {tc.error_counter} errors found")
