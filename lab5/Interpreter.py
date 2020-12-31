from AST import *
from SymbolTable import *
from Memory import *
from Exceptions import  *
from visit import *
import sys
from collections import defaultdict

sys.setrecursionlimit(10000)

opdict = defaultdict(lambda: None)

opdict['+'] = lambda x, y: x + y
opdict['-'] = lambda x, y: x - y
opdict['*'] = lambda x, y: x * y
opdict['/'] = lambda x, y: x / y

def matrix_operation(A, B, op):
    if len(A) == 0:
        return A
    elif not isinstance(A[0], list):
        return [op(a, b) for (a, b) in zip(A, B)]
    else:
        return [matrix_operation(a_row, b_row, op) for (a_row, b_row) in zip(A, B)]

opdict['.+'] = lambda A, B: matrix_operation(A, B, opdict['+'])
opdict['.-'] = lambda A, B: matrix_operation(A, B, opdict['-'])
opdict['.*'] = lambda A, B: matrix_operation(A, B, opdict['*'])
opdict['./'] = lambda A, B: matrix_operation(A, B, opdict['/'])

opdict['=='] = lambda x, y: x == y
opdict['!='] = lambda x, y: x != y
opdict['<']  = lambda x, y: x < y
opdict['>']  = lambda x, y: x > y
opdict['<='] = lambda x, y: x <= y
opdict['>='] = lambda x, y: x >= y

opdict['+='] = lambda x, y: x + y
opdict['-='] = lambda x, y: x - y
opdict['*='] = lambda x, y: x * y
opdict['/='] = lambda x, y: x / y

unopdict = {
    '-':  lambda x: -x,
    '\'': lambda m: [[l[i] for l in m] for i in range(len(m[0]))]
}

class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return opdict[node.op](r1, r2)

    @when(Start)
    def visit(self, node: Start):
        try:
            for ins in node.instructions:
                ins.accept(self)
        except ReturnValueException as val:
            memory = self.memory_stack.memories[-1]
            if memory.name == "program":
                print(f"Program returned with {val}")
            else:
                raise ReturnValueException(val)

    @when(Intnum)
    def visit(self, node):
        return node.term
    
    @when(Floatnum)
    def visit(self, node):
        return node.term
        
    @when(String)
    def visit(self, node):
        return node.term

    @when(Id)
    def visit(self, node):
        return self.memory_stack.get(node.ref)

    @when(ArrayRef)
    def visit(self, node):
        arr = self.memory_stack.get(node.ref)
        if len(node.indices) == 1:
            return arr[node.indices[0].accept(self)]
        else:
            return arr[node.indices[0].accept(self)][node.indices[1].accept(self)]

    @when(ArrayRange)
    def visit(self, node):
        arr = self.memory_stack.get(node.ref)
        left, right = node.range_.accept(self)
        return arr[left:right]

    @when(Assign)
    def visit(self, node):
        right_val = node.right.accept(self)
        to_set_val = None

        if node.op == '=':
            to_set_val = right_val
        else:
            left_val = node.left.accept(self)
            to_set_val = opdict[node.op](left_val, right_val)
            
        if isinstance(node.left, Id):
            self.memory_stack.set(node.left.ref, to_set_val)
        elif isinstance(node.left, ArrayRef):
            arr = self.memory_stack.get(node.left.ref)
            if len(node.left.indices) == 1:
                arr[node.left.indices[0].accept(self)] = to_set_val
            else:
                arr[node.left.indices[0].accept(self)][node.left.indices[1].accept(self)] = to_set_val
    
    @when(UnOp)
    def visit(self, node):
        return unopdict[node.op](node.expr.accept(self))

    @when(If)
    def visit(self, node):
        if node.condition.accept(self) != 0:
            self.memory_stack.push(Memory("if"))
            try:
                node.instructions.accept(self)
                self.memory_stack.pop()
            except ReturnValueException as val:
                self.memory_stack.pop()
                raise ReturnValueException(val)

    @when(IfElse)
    def visit(self, node):
        if node.condition.accept(self) != 0:
            self.memory_stack.push(Memory("if"))
            try:
                node.if_instructions.accept(self)
                self.memory_stack.pop()
            except ReturnValueException as val:
                self.memory_stack.pop()
                raise ReturnValueException(val)
        else:
            self.memory_stack.push(Memory("else"))
            try:
                node.else_instructions.accept(self)
                self.memory_stack.pop()
            except ReturnValueException as val:
                self.memory_stack.pop()
                raise ReturnValueException(val)
    
    @when(While)
    def visit(self, node: While):
        self.memory_stack.push(Memory("while"))
        try:
            while node.condition.accept(self):
                try:
                    node.instructions.accept(self)
                except BreakException:
                    break
                except ContinueException:
                    pass
            self.memory_stack.pop()
        except ReturnValueException as val:
            self.memory_stack.pop()
            raise ReturnValueException(val)
    
    @when(For)
    def visit(self, node: For):
        range_name = node.ref.ref
        range_start, range_end = node.range_.accept(self)

        self.memory_stack.push(Memory("for"))
        self.memory_stack.insert(range_name, range_start)
        try:
            while self.memory_stack.get(range_name) < range_end:
                try:
                    node.instructions.accept(self)
                except BreakException:
                    break
                except ContinueException:
                    pass
                self.memory_stack.set(range_name, self.memory_stack.get(range_name) + 1)
            self.memory_stack.pop()
        except ReturnValueException as val:
            self.memory_stack.pop()
            raise ReturnValueException(val)
        
    @when(Return)
    def visit(self, node: Return):
        raise ReturnValueException(node.value.accept(self))

    @when(Print)
    def visit(self, node: Print):
        print(", ".join([str(val) for val in node.value.accept(self)]))

    @when(PrintArray)
    def visit(self, node: Array):
        return [val.accept(self) for val in node.values]

    @when(Break)
    def visit(self, node):
        raise BreakException()

    @when(Continue)
    def visit(self, node):
        raise ContinueException()
    
    @when(Zeros)
    def visit(self, node: Zeros):
        rows = node.rows.accept(self)
        columns = node.columns.accept(self)
        return [[0 for _ in range(columns)] for _ in range(rows)] 
    
    @when(Ones)
    def visit(self, node: Ones):
        rows = node.rows.accept(self)
        columns = node.columns.accept(self)
        return [[1 for _ in range(columns)] for _ in range(rows)] 
            
    @when(Eye)
    def visit(self, node: Eye):
        rows = node.rows.accept(self)
        columns = node.columns.accept(self)
        return [[1 if i == j else 0 for i in range(columns)] for j in range(rows)]
            
    @when(Array)
    def visit(self, node: Array):
        return [val.accept(self) for val in node.values]
    
    @when(Range)
    def visit(self, node: Range):
        return (node.left.accept(self), node.right.accept(self))