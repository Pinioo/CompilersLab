import AST

indent_representation = "|  "


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    @addToClass(AST.Root)
    def printTree(self, indent=0) -> str:
        return self.instructions.printTree(indent)

    @addToClass(AST.Start)
    def printTree(self, indent) -> str:
        return "".join(
            instruction.printTree(indent) for instruction in self.instructions
        )

    @addToClass(AST.Block)
    def printTree(self, indent) -> str:
        return self.instructions.printTree(indent)

    @addToClass(AST.Struct)
    def printTree(self, indent) -> str:
        return self.instructions.printTree(indent)

    @addToClass(AST.Term)
    def printTree(self, indent) -> str:
        return ( 
            indent * indent_representation + 
            str(self.term) + '\n'
        )

    @addToClass(AST.Id)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + 
            self.ref + '\n'
        )

    @addToClass(AST.ArrayRef)
    def printTree(self, indent) -> str:
        return ( 
            indent * indent_representation + "ARRAY_REF\n" + 
            (indent+1) * indent_representation + self.ref + '\n' 
            + self.indices.printTree(indent+1)
        )

    @addToClass(AST.BinOp)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + self.op + '\n' + 
            self.left.printTree(indent+1) + 
            self.right.printTree(indent+1)
        )
      
    @addToClass(AST.UnOp)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + self.op + '\n' + 
            self.expr.printTree(indent+1)
        )

    @addToClass(AST.If)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "IF\n" + 
            self.condition.printTree(indent+1) +
            self.instructions.printTree(indent+1)
        )

    @addToClass(AST.IfElse)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "IF\n" + 
            self.condition.printTree(indent+1) + 
            self.if_instructions.printTree(indent+1) + 
            indent * indent_representation + "ELSE\n" +
            self.else_instructions.printTree(indent+1)
        )


    @addToClass(AST.While)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "WHILE\n" +
            self.condition.printTree(indent+1) +
            self.instructions.printTree(indent+1)
        )

    @addToClass(AST.For)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "FOR\n" + 
            self.ref.printTree(indent+1) +
            self.range_.printTree(indent+1) +
            self.instructions.printTree(indent+1)
        )

    @addToClass(AST.Print)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "RETURN\n" +
            self.value.printTree(indent+1)
        )

    @addToClass(AST.Print)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "PRINT\n" +
            self.value.printTree(indent+1)
        )

    @addToClass(AST.Break)
    def printTree(self, indent) -> str:
        return indent * indent_representation + "BREAK\n"

    @addToClass(AST.Continue)
    def printTree(self, indent) -> str:
        return indent * indent_representation + "CONTINUE\n"

    @addToClass(AST.Ones)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "ONES\n" +
            self.argument.printTree(indent+1)
        )

    @addToClass(AST.Zeros)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "ZEROS\n" +
            self.argument.printTree(indent+1)
        )

    @addToClass(AST.Eye)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "EYE\n" +
            self.argument.printTree(indent+1)
        )

    @addToClass(AST.Array)
    def printTree(self, indent) -> str:
        return ( 
            indent * indent_representation + "ARRAY\n" + 
            "".join(
                instruction.printTree(indent) for instruction in self.values
            )
        )

    @addToClass(AST.Range)
    def printTree(self, indent) -> str:
        return (
            indent * indent_representation + "RANGE\n" +
            self.left.printTree(indent+1) +
            self.right.printTree(indent+1)
        )