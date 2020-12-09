import AST
import SymbolTable
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

class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        pass

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r