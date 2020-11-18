import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:
    @addToClass(AST.Root)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.Start)
    def printTree(self, indent):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Block)
    def printTree(self, indent):
        # print(indent * "|  " + "BLOCK")     # ???
        # self.instructions.printTree(indent+1)
        self.instructions.printTree(indent)

    @addToClass(AST.Struct)
    def printTree(self, indent):
        self.instructions.printTree(indent)

    @addToClass(AST.Term)
    def printTree(self, indent):
        print(indent * "|  " + str(self.term))

    @addToClass(AST.Id)
    def printTree(self, indent):
        print(indent * "|  " + self.ref)

    @addToClass(AST.ArrayRef)
    def printTree(self, indent):
        print(indent * "|  " + "ARRAY_REF")
        print((indent+1) * "|  " + self.ref)
        self.indices.printTree(indent+1)

    @addToClass(AST.BinOp)
    def printTree(self, indent):
        print(indent * "|  " + self.op)
        self.left.printTree(indent+1) 
        self.right.printTree(indent+1)
      
    @addToClass(AST.UnOp)
    def printTree(self, indent):
        print(indent * "|  " + self.op)
        self.expr.printTree(indent+1)

    @addToClass(AST.If)
    def printTree(self, indent):
        print(indent * "|  " + "IF")
        self.condition.printTree(indent+1)
        self.instructions.print(indent+1)

    @addToClass(AST.IfElse)
    def printTree(self, indent):
        print(indent * "|  " + "IF")
        self.condition.printTree(indent+1)
        self.if_instructions.printTree(indent+1)
        print(indent * "|  " + "ELSE")
        self.else_instructions.printTree(indent+1)


    @addToClass(AST.While)
    def printTree(self, indent):
        print(indent * "|  " + "WHILE")
        self.condition.printTree(indent+1)
        self.instructions.printTree(indent+1)

    @addToClass(AST.For)
    def printTree(self, indent):
        print(indent * "|  " + "FOR")
        self.ref.printTree(indent+1)
        self.range_.printTree(indent+1)
        self.instructions.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent):
        print(indent * "|  " + "RETURN")
        self.value.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent):
        print(indent * "|  " + "PRINT")
        self.value.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent):
        print(indent * "|  " + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent):
        print(indent * "|  " + "CONTINUE")

    @addToClass(AST.Ones)
    def printTree(self, indent):
        print(indent * "|  " + "ONES")
        self.argument.printTree(indent+1)

    @addToClass(AST.Zeros)
    def printTree(self, indent):
        print(indent * "|  " + "ZEROS")
        self.argument.printTree(indent+1)

    @addToClass(AST.Eye)
    def printTree(self, indent):
        print(indent * "|  " + "EYE")
        self.argument.printTree(indent+1)

    @addToClass(AST.ArrayInterior)
    def printTree(self, indent):
        for instruction in self.values:
            instruction.printTree(indent)

    @addToClass(AST.Array)
    def printTree(self, indent):
        print(indent * "|  " + "ARRAY")
        self.interior.printTree(indent+1)

    @addToClass(AST.Range)
    def printTree(self, indent):
        print(indent * "|  " + "RANGE")
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)