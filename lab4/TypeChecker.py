from collections import defaultdict
import functools

from AST import *
from SymbolTable import SymbolTable

INTNUM = 'INTNUM'
FLOATNUM = 'FLOATNUM'
STRING = 'STRING'
ARRAY = 'ARRAY'
MATRIX = 'MATRIX'
RANGE = 'RANGE'

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

ttype['+'][INTNUM][INTNUM] = INTNUM
ttype['+'][INTNUM][FLOATNUM] = FLOATNUM
ttype['+'][FLOATNUM][INTNUM] = FLOATNUM
ttype['+'][FLOATNUM][FLOATNUM] = FLOATNUM
ttype['+'][STRING][STRING] = STRING
ttype['+'][ARRAY][ARRAY] = ARRAY

ttype['-'] = ttype['*'] = ttype['/'] = ttype['+']
ttype['+='] = ttype['-='] = ttype['*='] = ttype['/='] = ttype['+']

ttype['.+'][ARRAY][ARRAY] = ARRAY
ttype['.+'][MATRIX][MATRIX] = MATRIX

ttype['.-'] = ttype['.*'] = ttype['./'] = ttype['.+']

ttype['=='][INTNUM][INTNUM] = INTNUM
ttype['=='][INTNUM][FLOATNUM] = INTNUM
ttype['=='][FLOATNUM][INTNUM] = INTNUM
ttype['=='][FLOATNUM][FLOATNUM] = INTNUM
ttype['=='][STRING][STRING] = INTNUM
ttype['=='][ARRAY][ARRAY] = INTNUM
ttype['=='][MATRIX][MATRIX] = INTNUM

ttype['!='] = ttype['<'] = ttype['>'] = ttype['<='] = ttype['>='] = ttype['==']

utype = defaultdict(lambda: defaultdict(lambda: None))

utype['-'][ARRAY] = ARRAY
utype['-'][MATRIX] = MATRIX
utype['-'][INTNUM] = INTNUM
utype['-'][FLOATNUM] = FLOATNUM

utype['\''][MATRIX] = MATRIX

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        return visitor(node)


    # def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
    #     if isinstance(node, list):
    #         for elem in node:
    #             self.visit(elem)
    #     else:
    #         for child in node.children:
    #             if isinstance(child, list):
    #                 for item in child:
    #                     if isinstance(item, AST.Node):
    #                         self.visit(item)
    #             elif isinstance(child, AST.Node):
    #                 self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'global')

    def visit_Start(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Block(self, node):
        for instruction in node.instructions: # symbol_table
            self.visit(instruction)

    def visit_Struct(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Term(self, node):
        return node.term.type

    def visit_Id(self, node):
        return self.symbol_table.get(node.ref)

    def visit_ArrayRef(self, node):
        arr = self.symbol_table.get(node.ref)
        ind_types = [self.visit(i) for i in node.indices.values]
        if not all([t == INTNUM for t in ind_types]):
            print("Index not INTNUM")
        if arr.type == ARRAY:
            if len(ind_types) != 1:
                print("Too many indexes for ARRAY")
            if isinstance(node.indices.values[0], Term): #TODO
                arr_len = len(arr.value)
                if node.indices.values[0].term >= arr_len or node.indices.values[0].term < 0:
                    print('Index out of range')
                return self.visit(arr.value[node.indices.values[0]])
            else:
                return None

        elif arr.type == MATRIX:
            row_i = node.indices.values[0].term
            col_j = node.indices.values[1].term
            if len(ind_types) != 2:
                print("Invalid indexes number for MATRIX")    
            if isinstance(node.indices.values[0], Term): #TODO
                mat_rows = len(arr.value.values)
                mat_columns = len(arr.value.values[0].values)
                if row_i >= mat_rows or row_i < 0:
                    print('Index out of range')
                if col_j >= mat_columns or col_j < 0:
                    print('Index out of range')
                return self.visit(arr.value[node.indices.values[0]])
            
        else:
            return None

    def visit_ArrayRange(self, node):
        arr = self.symbol_table.get(node.ref)
        if arr.type == ARRAY:
            if isInstance(node.left, Term) and node.left < 0:
                print('Index out of range')
                if isInstance(node.left, Term) and node.right >= len(arr.value.values):
                    print('Index out of range')
                    return self.visit(Array(arr.value.values[node.left : node.right]))
            return None
        else:
            print('Range can be used only with ARRAY')

    def visit_BinOp(self, node):
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        result = ttype[op][type1][type2]
        if result is None:
            print(f'{type1} {op} {type2} is invalid operation')
        return result

    def visit_Variable(self, node):
        pass
    
    def visit_UnOp(self, node):
        result = utype[node.op][self.visit(node.expr)]
        if result is None:
            print(f'{type1} {op} is invalid operation')
        return result

    def visit_If(self, node):
        result = self.visit(node.condition)
        if result != INTNUM:
            print(f'If condition is invalid')
        return result

    def visit_IfElse(self, node):
        result = self.visit(node.condition)
        if result != INTNUM:
            print(f'IfElse condition is invalid')
        return result
    
    def visit_While(self, node):
        result = self.visit(node.condition)
        if result != INTNUM:
            print(f'While condition is invalid')
        return result
    
    def visit_For(self, node):
        type_range = self.visit(node.range_)
        if type_range != RANGE:
            return None

    def visit_Return(self, node):
        type1 = self.visit(node.value)
        return None

    def visit_Print(self, node):
        type1 = self.visit(node.value)
        return None

    def visit_Break(self, node):
        pass
    
    def visit_Continue(self, node):
        pass
    
    def visit_Zeros(self, node):
        type1 = self.visit(node.rows)
        type2 = self.visit(node.columns) if node.rows != node.columns else type1
        if type1 != INTNUM or type2 != INTNUM:
            print(f'Zeros({type1}, {type2}); arguments must be INTNUM')
            return None
        elif node.rows.term <= 0 or node.columns.term <= 0:
            print(f'Zeros({type1}, {type2}); arguments must be positive')
            return None
        else:
            return MATRIX
    
    def visit_Ones(self, node):
        type1 = self.visit(node.rows)
        type2 = self.visit(node.columns) if node.rows != node.columns else type1
        if type1 != INTNUM or type2 != INTNUM:
            print(f'Ones({type1}, {type2}); arguments must be INTNUM')
            return None
        elif node.rows.term <= 0 or node.columns.term <= 0:
            print(f'Ones({type1}, {type2}); arguments must be positive')
            return None
        else:
            return MATRIX
            
    def visit_Eye(self, node):
        type1 = self.visit(node.rows)
        type2 = self.visit(node.columns) if node.rows != node.columns else type1
        if type1 != INTNUM or type2 != INTNUM:
            print(f'Eye({type1}, {type2}); arguments must be INTNUM')
            return None
        elif node.rows.term <= 0 or node.columns.term <= 0:
            print(f'Eye({type1}, {type2}); arguments must be positive')
            return None
        else:
            return MATRIX
            
    def visit_Array(self, node):
        val_types = [self.visit(nd) for nd in node.values]
        if None in val_types or MATRIX in val_types:
            return None
        if ARRAY in val_types:
            # Possible Matrix
            if all([x == ARRAY for x in val_types]):
                # Matrix
                length = len(val_types)
                if length == 0 or any([len(x.values) != length for x in node.values]):
                    print('Cannot create matrix with non rectangluar shape')
                    return None
                    
                return MATRIX
            else:
                print("")
        else:
            # Array
            return ARRAY
    
    def visit_Range(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if type1 != INTNUM or type2 != INTNUM:
            print(f'{type1}:{type2} is invalid range')
            return None
        else:
            return RANGE