from collections import defaultdict
import functools

from AST import *
from SymbolTable import *

INTNUM = "INTNUM"
FLOATNUM = "FLOATNUM"
STRING = "STRING"
ARRAY = "ARRAY"
MATRIX = "MATRIX"
RANGE = "RANGE"

# Binary operations types
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

# Unary operations types
utype = defaultdict(lambda: defaultdict(lambda: None))

utype['-'][ARRAY] = ARRAY
utype['-'][MATRIX] = MATRIX
utype['-'][INTNUM] = INTNUM
utype['-'][FLOATNUM] = FLOATNUM

utype['\''][MATRIX] = MATRIX


class NodeVisitor(object):
    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, None)
        return visitor(node)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "outside_loop")
        self.error_counter = 0
        self.create_child_scopes = True

    def print_err(self, node, message):
        print(f"[line {node.line}]: {message}")
        self.error_counter += 1

    def visit_Start(self, node):
        if self.create_child_scopes:
            self.symbol_table = self.symbol_table.create_child_scope(self.symbol_table.name)
            created_child_scope = True
        else:
            self.create_child_scopes = True
            created_child_scope = False

        for instruction in node.instructions:
            self.visit(instruction)

        if created_child_scope:
            self.symbol_table = self.symbol_table.parent

    def visit_Intnum(self, node):
        return INTNUM
        
    def visit_Floatnum(self, node):
        return FLOATNUM
        
    def visit_String(self, node):
        return STRING

    def visit_Id(self, node):
        id_symbol = self.symbol_table.get(node.ref)
        if id_symbol is None:
            self.print_err(node, f"{node.ref} is undefined")
            return None
        else:
            return self.symbol_table.get(node.ref).type

    def visit_ArrayRef(self, node):
        arr = self.symbol_table.get(node.ref)
        if arr.type == ARRAY:
            if len(node.indices.values) != 1:
                self.print_err(node, "Too many indexes for ARRAY")
                return None
            index_node = node.indices.values[0]
            if self.visit(index_node) == INTNUM:
                # if isinstance(node.range_.left, Intnum)
                index = index_node.term
                arr_len = len(arr.value.values)
                if index >= arr_len or index < 0:
                    self.print_err(node, "Index out of range")
                    return None
                return self.visit(arr.value.values[index])
            else:
                self.print_err(node, "Index must be INTNUM")
                return None

        elif arr.type == MATRIX:
            if len(node.indices.values) != 2:
                self.print_err(node, "Invalid indexes number for MATRIX")    
                return None
            
            index1_node = node.indices.values[0]
            index2_node = node.indices.values[1]
            if self.visit(index1_node) == INTNUM and self.visit(index2_node) == INTNUM:
                row_i = index1_node.term
                col_j = index2_node.term
                mat_rows = len(arr.value.values)
                mat_columns = len(arr.value.values[0].values)
                if row_i >= mat_rows or row_i < 0:
                    self.print_err(node, "Index out of range")
                if col_j >= mat_columns or col_j < 0:
                    self.print_err(node, "Index out of range")
                return self.visit(arr.value.values[row_i].values[col_j])
            else:
                self.print_err(node, "Indexes must be INTNUM")
            
        else:
            return None

    # WRONG
    def visit_ArrayRange(self, node):
        arr = self.symbol_table.get(node.ref)
        if arr.type == ARRAY:
            if isinstance(node.range_.left, Intnum) and node.range_.left.term > len(arr.value.values):
                self.print_err(node, f"Index out of range")
                return None
            elif isinstance(node.range_.right, Intnum) and node.range_.right.term >= len(arr.value.values):
                self.print_err(node, f"Index out of range")
                return None
            elif isinstance(node.range_.left, Intnum) and isinstance(node.range_.right, Intnum):
                return self.visit(Array(arr.value.values[node.range_.left.term : node.range_.right.term]))
            else:
                # return Array("Undefined list") #TODO
                return self.print_err(node, "Ranged array can only use const range (for now)") 
        else:
            self.print_err(node, f"Range can be used only with ARRAY")
            return None

    
    def visit_Assign(self, node):
        r_type = self.visit(node.right)
        if r_type is None:
            return None
        if isinstance(node.left, Id):
            if node.op == "=":
                to_put = node.right
                if isinstance(node.right, Eye):
                    rows = node.right.rows.term
                    cols = node.right.columns.term
                    to_put = Array(
                        [Array(
                            [Intnum(1 if i == j else 0) for j in range(cols)]
                        ) for i in range(rows)]
                    )
                elif isinstance(node.right, Ones):
                    rows = node.right.rows.term
                    cols = node.right.columns.term
                    to_put = Array(
                        [Array(
                            [Intnum(1)] * cols
                        ) for _ in range(rows)]
                    )
                elif isinstance(node.right, Zeros):
                    rows = node.right.rows.term
                    cols = node.right.columns.term
                    to_put = Array(
                        [Array(
                            [Intnum(0)] * cols
                        ) for _ in range(rows)]
                    )
                self.symbol_table.put(
                    node.left.ref, 
                    VariableSymbol(node.left.ref, r_type, to_put)    
                )
                return r_type
            else:
                l_symbol = self.symbol_table.get(node.left.ref)
                if l_symbol is None:
                    self.print_err(node, f"{node.left.ref} is undefined")
                    return None
                l_type = l_symbol.type
                final_type = ttype[node.op][l_type][r_type]
                if final_type is None:
                    self.print_err(node, f"Incompatible types")
                l_symbol.type = final_type
                return final_type
            return None
            
        elif isinstance(node.left, ArrayRef):
            l_symbol = self.symbol_table.get(node.left.ref)
            if l_symbol is None:
                self.print_err(node, f"{node.left.ref} is undefined")
                return None
            l_type = l_symbol.type
            if l_type == ARRAY:
                arr = l_symbol.value
                index = node.indices.values[0].term
                if index < 0 or index >= len(arr.values):
                    self.print_err(node, "Index out of range")
                    return None
                if node.op == "=":
                    arr.values[index] = node.right
                    return r_type
                else:
                    final_type = ttype[node.op][self.visit(arr.values[index])][r_type]
                    if final_type is None:
                        self.print_err(node, f"Incompatible types")
                    return final_type

            if l_type == MATRIX:
                mat = l_symbol.value
                row_i = node.indices.values[0].term
                col_j = node.indices.values[1].term
                if row_i < 0 or row_i >= len(mat.values) or col_j < 0 or col_j >= len(mat.values[0].values):
                    self.print_err(node, "Index out of range")
                    return None
                if node.op == "=":
                    mat.values[row_i].values[col_j] = node.right
                    return r_type
                else:
                    final_type = ttype[node.op][self.visit(mat.values[row_i].values[col_j])][r_type]
                    if final_type is None:
                        self.print_err(node, f"Incompatible types")
                    return final_type

        elif isinstance(node.left, ArrayRange):
            pass

    def visit_BinOp(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op    = node.op
        result = ttype[op][type1][type2]
        if result is None:
            self.print_err(node, f"{type1} {op} {type2} is invalid operation")
        elif result == ARRAY:
            dims = []
            for arr_repr in [node.left, node.right]:
                if isinstance(arr_repr, Array):
                    arr = arr_repr
                elif isinstance(arr_repr, ArrayRange):
                    arr_full = self.symbol_table.get(arr_repr.ref).value
                    arr = Array(arr_full.values[arr_repr.range_.left:arr_repr.range_.right])
                elif isinstance(arr_repr, Id):
                    arr = self.symbol_table.get(arr_repr.ref)
                else:
                    self.print_err(node, "Arrays in BinOp must be Array, ArrayRange or Id")
                    return None
                dims.append(len(arr.values))

            if dims[0] != dims[1]:
                self.print_err(node, f"Dimensions {dims[0]} and {dims[1]} are incompatible")
                return None

        elif result == MATRIX:
            row_dims = []
            col_dims = []
            for mat_repr in [node.left, node.right]:
                if isinstance(mat_repr, Array):
                    mat = mat_repr
                elif isinstance(mat_repr, Id):
                    mat = self.symbol_table.get(mat_repr.ref).value
                else:
                    self.print_err(node, "Matrices in BinOp must be Matrix or Id")
                    return None
                row_dims.append(len(mat.values))
                col_dims.append(len(mat.values[0].values))

            if row_dims[0] != row_dims[1]:
                self.print_err(node, f"Dimensions {row_dims[0]} and {row_dims[1]} are incompatible")
                return None
                
            if col_dims[0] != col_dims[1]:
                self.print_err(node, f"Dimensions {col_dims[0]} and {col_dims[1]} are incompatible")
                return None
        
        return result

    def visit_Variable(self, node):
        pass
    
    def visit_UnOp(self, node):
        result = utype[node.op][self.visit(node.expr)]
        if result is None:
            self.print_err(node, f"{type1} {op} is invalid operation")
        return result

    def visit_If(self, node):
        result = self.visit(node.condition)
        if result != INTNUM:
            self.print_err(node, f"If condition is invalid")
        self.visit(node.instructions)
        return result

    def visit_IfElse(self, node):
        result = self.visit(node.condition)
        if result != INTNUM:
            self.print_err(node, f"IfElse condition is invalid")
        self.visit(node.if_instructions)
        self.visit(node.else_instructions)
    
    def visit_While(self, node):
        result = self.visit(node.condition)
        if result != INTNUM:
            self.print_err(node, f"While condition is invalid")
        self.symbol_table = self.symbol_table.create_child_scope('inside_loop')
        self.create_child_scopes = False

        self.visit(node.instructions)

        self.create_child_scopes = True
        self.symbol_table = self.symbol_table.parent
    
    def visit_For(self, node):
        type_range = self.visit(node.range_)
        if type_range != RANGE:
            self.print_err(node, f"For range is invalid")
        else:
            self.symbol_table.put(
                node.ref.ref,
                VariableSymbol(node.ref.ref, INTNUM)
            )
        self.symbol_table = self.symbol_table.create_child_scope('inside_loop')
        self.create_child_scopes = False

        self.visit(node.instructions)

        self.create_child_scopes = True
        self.symbol_table = self.symbol_table.parent
        
    def visit_Return(self, node):
        self.visit(node.value)

    def visit_Print(self, node):
        self.visit(node.value)

    def visit_Break(self, node):
        if self.symbol_table.name != 'inside_loop':
            self.print_err(node, 'BREAK outside loop')
    
    def visit_Continue(self, node):
        if self.symbol_table.name != 'inside_loop':
            self.print_err(node, 'CONTINUE outside loop')
    
    def visit_Zeros(self, node):
        type1 = self.visit(node.rows)
        type2 = self.visit(node.columns) if node.rows != node.columns else type1
        if type1 != INTNUM or type2 != INTNUM:
            self.print_err(node, f"Zeros({type1}, {type2}); arguments must be INTNUM")
            return None
        elif node.rows.term <= 0 or node.columns.term <= 0:
            self.print_err(node, f"Zeros({type1}, {type2}); arguments must be positive")
            return None
        else:
            return MATRIX
    
    def visit_Ones(self, node):
        type1 = self.visit(node.rows)
        type2 = self.visit(node.columns) if node.rows != node.columns else type1
        if type1 != INTNUM or type2 != INTNUM:
            self.print_err(node, f"Ones({type1}, {type2}); arguments must be INTNUM")
            return None
        elif node.rows.term <= 0 or node.columns.term <= 0:
            self.print_err(node, f"Ones({type1}, {type2}); arguments must be positive")
            return None
        else:
            return MATRIX
            
    def visit_Eye(self, node):
        type1 = self.visit(node.rows)
        type2 = self.visit(node.columns) if node.rows != node.columns else type1
        if type1 != INTNUM or type2 != INTNUM:
            self.print_err(node, f"Eye({type1}, {type2}); arguments must be INTNUM")
            return None
        elif node.rows.term <= 0 or node.columns.term <= 0:
            self.print_err(node, f"Eye({type1}, {type2}); arguments must be positive")
            return None
        else:
            return MATRIX
            
    def visit_Array(self, node):
        val_types = [self.visit(nd) for nd in node.values]
        if None in val_types:
            return None
        elif MATRIX in val_types:
            self.print_err(node, 'MATRIX cannot be inside ARRAY or MATRIX')
            return None
        elif ARRAY in val_types:
            # Possible Matrix
            if all([x == ARRAY for x in val_types]):
                # Matrix
                length = len(node.values[0].values)
                if length == 0 or any([len(x.values) != length for x in node.values]):
                    self.print_err(node, "Cannot create matrix with non rectangluar shape")
                    return None
                    
                return MATRIX
            else:
                self.print_err(node, f"ARRAY cannot be inside ARRAY that is not MATRIX")
        else:
            # Array
            return ARRAY
    
    def visit_Range(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if type1 != INTNUM or type2 != INTNUM:
            self.print_err(node, f"{type1}:{type2} is invalid range")
            return None
        else:
            return RANGE