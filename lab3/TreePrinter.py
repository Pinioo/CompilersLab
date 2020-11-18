import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:
    @addToClass(AST.Root)
    def printTree(self, indent=0):
        print("ROOT")
        self.instructions.printTree(indent)

    @addToClass(AST.Start)
    def printTree(self, indent):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Block)
    def printTree(self, indent):
        print(indent * "|   " + "+-- {")
        self.instructions.printTree(indent+1)
        print(indent * "|   " + "+-- }")

    @addToClass(AST.FinishedStruct)
    def printTree(self, indent):
        self.instructions.printTree(indent)
        print(indent * "|   " + "+-- ;")

    @addToClass(AST.Term)
    def printTree(self, indent):
        print(indent * "|   " + "+-- " + str(self.term))

    @addToClass(AST.Id)
    def printTree(self, indent):
        print(indent * "|   " + "+-- " + self.ref)

    @addToClass(AST.ArrayRef)
    def printTree(self, indent):
        print(indent * "|   " + "+-- " + self.ref)
        print(indent * "|   " + "+-- [")
        self.indices.printTree(indent+1)
        print(indent * "|   " + "+-- ]")

    @addToClass(AST.Assign)
    def printTree(self, indent):
        self.left.printTree(indent+1)
        print(indent * "|   " + "+-- " + self.op)
        self.right.printTree(indent+1)

    @addToClass(AST.BinOp)
    def printTree(self, indent):
        self.left.printTree(indent+1)
        print(indent * "|   " + "+-- " + self.op) 
        self.right.printTree(indent+1)

    @addToClass(AST.MatOp)
    def printTree(self, indent):
        self.left.printTree(indent+1)
        print(indent * "|   " + "+-- " + self.op)
        self.right.printTree(indent+1)
    
    @addToClass(AST.LogicOp)
    def printTree(self, indent):
        self.left.printTree(indent+1)
        print(indent * "|   " + "+-- " + self.op)
        self.right.printTree(indent+1)
        
    @addToClass(AST.UnLeftExpr)
    def printTree(self, indent):
        print(indent * "|   " + "+-- " + self.op)
        self.right.printTree(indent+1)

    @addToClass(AST.UnRightExpr)
    def printTree(self, indent):
        self.left.printTree(indent+1)
        print(indent * "|   " + "+-- " + self.op)

    @addToClass(AST.If)
    def printTree(self, indent):
        print(indent * "|   " + "+-- IF")
        print(indent * "|   " + "+-- (")
        self.condition.printTree(indent+1)
        print(indent * "|   " + "+-- )")
        self.instructions.print(indent+1)

    @addToClass(AST.IfElse)
    def printTree(self, indent):
        print(indent * "|   " + "+-- IF")
        print(indent * "|   " + "+-- (")
        self.condition.printTree(indent+1)
        print(indent * "|   " + "+-- )")
        self.if_instructions.printTree(indent+1)
        print(indent * "|   " + "+-- ELSE")
        self.else_instructions.printTree(indent+1)


    @addToClass(AST.While)
    def printTree(self, indent):
        print(indent * "|   " + "+-- WHILE")
        print(indent * "|   " + "+-- (")
        self.condition.printTree(indent+1)
        print(indent * "|   " + "+-- )")
        self.instructions.printTree(indent+1)

    @addToClass(AST.For)
    def printTree(self, indent):
        print(indent * "|   " + "+-- FOR")
        print(indent * "|   " + "+-- =")
        self.range_from.printTree(indent+1)
        print(indent * "|   " + "+-- :")
        self.range_to.printTree(indent+1)
        self.instructions.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent):
        print(indent * "|   " + "+-- RETURN")
        self.value.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent):
        print(indent * "|   " + "+-- PRINT")
        self.value.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent):
        print(indent * "|   " + "+-- CONTINUE")

    @addToClass(AST.Continue)
    def printTree(self, indent):
        print(indent * "|   " + "+-- CONTINUE")

    @addToClass(AST.Ones)
    def printTree(self, indent):
        print(indent * "|   " + "+-- ONES")
        print(indent * "|   " + "+-- (")
        self.argument.printTree(indent+1)
        print(indent * "|   " + "+-- )")

    @addToClass(AST.Zeros)
    def printTree(self, indent):
        print(indent * "|   " + "+-- ZEROS")
        print(indent * "|   " + "+-- (")
        self.argument.printTree(indent+1)
        print(indent * "|   " + "+-- )")

    @addToClass(AST.Eye)
    def printTree(self, indent):
        print(indent * "|   " + "+-- EYE")
        print(indent * "|   " + "+-- (")
        self.argument.printTree(indent+1)
        print(indent * "|   " + "+-- )")

    @addToClass(AST.ArrayInterior)
    def printTree(self, indent):
        for i, instruction in enumerate(self.values):
            instruction.printTree(indent)
            if i < len(self.values) - 1:
                print(indent * "|   " + "+-- ,")

    @addToClass(AST.Array)
    def printTree(self, indent):
        print(indent * "|   " + "+-- [")
        self.interior.printTree(indent+1)
        print(indent * "|   " + "+-- ]")