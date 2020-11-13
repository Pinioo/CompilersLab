import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, cls.__name__, func)
        return func
    return decorator

class TreePrinter:
    @addToClass(AST.Term)
    def printTree(self, indent):
        print(indent * "\t" + "+---" + self.term)

    @addToClass(AST.BinExpr)
    def printTree(self, indent):
        print(indent * "\t" + "+---" + self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.UnLeftExpr)
    def printTree(self, indent):
        print(indent * "\t" + "+---" + self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)
    
    