import sys
import scanner
import Mparser
from TreePrinter import TreePrinter
from TreeGrapher import draw_tree_from_text

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    
    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    draw_tree_from_text(ast.printTree())
