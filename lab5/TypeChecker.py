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
UNKNOWN_TERM = "UNKNOWN_TERM"
UNKNOWN_ARRAY = "UNKNOWN_ARRAY"

# Binary operations types
ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

ttype['+'][INTNUM][INTNUM] = INTNUM
ttype['+'][INTNUM][FLOATNUM] = FLOATNUM
ttype['+'][INTNUM][UNKNOWN_TERM] = UNKNOWN_TERM
ttype['+'][FLOATNUM][INTNUM] = FLOATNUM
ttype['+'][FLOATNUM][FLOATNUM] = FLOATNUM
ttype['+'][FLOATNUM][UNKNOWN_TERM] = UNKNOWN_TERM
ttype['+'][STRING][STRING] = STRING
ttype['+'][STRING][UNKNOWN_TERM] = UNKNOWN_TERM
ttype['+'][UNKNOWN_TERM][INTNUM] = UNKNOWN_TERM
ttype['+'][UNKNOWN_TERM][FLOATNUM] = UNKNOWN_TERM
ttype['+'][UNKNOWN_TERM][STRING] = UNKNOWN_TERM
ttype['+'][UNKNOWN_TERM][UNKNOWN_TERM] = UNKNOWN_TERM

ttype['-'] = ttype['*'] = ttype['/'] = ttype['+']
ttype['+='] = ttype['-='] = ttype['*='] = ttype['/='] = ttype['+']

ttype['*'][STRING][INTNUM] = STRING
ttype['*'][INTNUM][STRING] = STRING

ttype['.+'][ARRAY][ARRAY] = ARRAY
ttype['.+'][ARRAY][UNKNOWN_ARRAY] = UNKNOWN_ARRAY
ttype['.+'][UNKNOWN_ARRAY][ARRAY] = UNKNOWN_ARRAY
ttype['.+'][UNKNOWN_ARRAY][UNKNOWN_ARRAY] = UNKNOWN_ARRAY
ttype['.+'][MATRIX][MATRIX] = MATRIX

ttype['.-'] = ttype['.*'] = ttype['./'] = ttype['.+']

ttype['=='][INTNUM][INTNUM] = INTNUM
ttype['=='][INTNUM][FLOATNUM] = INTNUM
ttype['=='][INTNUM][UNKNOWN_TERM] = INTNUM
ttype['=='][FLOATNUM][INTNUM] = INTNUM
ttype['=='][FLOATNUM][FLOATNUM] = INTNUM
ttype['=='][FLOATNUM][UNKNOWN_TERM] = INTNUM
ttype['=='][STRING][STRING] = INTNUM
ttype['=='][STRING][UNKNOWN_TERM] = INTNUM
ttype['=='][ARRAY][ARRAY] = INTNUM
ttype['=='][ARRAY][UNKNOWN_ARRAY] = INTNUM
ttype['=='][MATRIX][MATRIX] = INTNUM
ttype['=='][UNKNOWN_TERM][INTNUM] = INTNUM
ttype['=='][UNKNOWN_TERM][FLOATNUM] = INTNUM
ttype['=='][UNKNOWN_TERM][STRING] = INTNUM
ttype['=='][UNKNOWN_TERM][UNKNOWN_TERM] = INTNUM
ttype['=='][UNKNOWN_ARRAY][ARRAY] = INTNUM
ttype['=='][UNKNOWN_ARRAY][UNKNOWN_ARRAY] = INTNUM

ttype['!='] = ttype['<'] = ttype['>'] = ttype['<='] = ttype['>='] = ttype['==']

# Unary operations types
utype = defaultdict(lambda: defaultdict(lambda: None))

utype['-'][ARRAY] = ARRAY
utype['-'][MATRIX] = MATRIX
utype['-'][INTNUM] = INTNUM
utype['-'][FLOATNUM] = FLOATNUM
utype['-'][UNKNOWN_TERM] = UNKNOWN_TERM

utype['\''][MATRIX] = MATRIX


class NodeVisitor(object):
    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, None)
        return visitor(node)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None)
        self.error_counter = 0
        self.scope = "outside_loop"

    def print_err(self, node, message):
        print(f"[line {node.line}]: {message}")
        self.error_counter += 1

    def visit_Start(self, node):
        self.symbol_table = self.symbol_table.create_child_scope()

        for instruction in node.instructions:
            self.visit(instruction)

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

        if len(node.indices.values) > 2:
            self.print_err(node, "More than 2 indexes")       
            return None
        elif arr is None:
            self.print_err(node, f"{node.ref} is undefined")
            return None
        elif arr.type == ARRAY or arr.type == UNKNOWN_ARRAY:
            if len(node.indices.values) != 1:
                self.print_err(node, "Too many indexes for ARRAY")
                return None
            index_node = node.indices.values[0]
            if self.visit(index_node) not in [INTNUM, UNKNOWN_TERM]:
                self.print_err(node, "Index must be INTNUM")
                return None

            if isinstance(index_node, Intnum) and not arr.type == UNKNOWN_ARRAY and not isinstance(arr.value, ArrayRange):
                index = index_node.term
                arr_len = len(arr.value.values)
                if index >= arr_len or index < 0:
                    self.print_err(node, "Index out of range")
                    return None
                return self.visit(arr.value.values[index])
            else:
                return UNKNOWN_TERM

        elif arr.type == MATRIX:
            if len(node.indices.values) < 2:
                self.print_err(node, "Not enough indexes for MATRIX")    
                return None
            elif len(node.indices.values) > 2:
                self.print_err(node, "Too many indexes for MATRIX")    
                return None
            
            index1_node = node.indices.values[0]
            index2_node = node.indices.values[1]
            if (self.visit(index1_node) not in [INTNUM, UNKNOWN_TERM] 
                    or self.visit(index2_node) not in [INTNUM, UNKNOWN_TERM]):
                self.print_err(node, "Index must be INTNUM")
                return None

            if isinstance(index1_node, Intnum):
                row_i = index1_node.term
                mat_rows = len(arr.value.values)
                if row_i >= mat_rows or row_i < 0:
                    self.print_err(node, "First index out of range")
                    return None

            if isinstance(index2_node, Intnum):
                col_j = index2_node.term
                mat_columns = len(arr.value.values[0].values)
                if col_j >= mat_columns or col_j < 0:
                    self.print_err(node, "Second index out of range")
                    return None
            
            if isinstance(index1_node, Intnum) and isinstance(index2_node, Intnum): 
                return self.visit(arr.value.values[row_i].values[col_j])
            else:
                return UNKNOWN_TERM

        else:
            self.print_err(node, f"Indexes list can be used only for ARRAY and MATRIX")
            return None

    def visit_ArrayRange(self, node):
        arr = self.symbol_table.get(node.ref)
        if arr.type == ARRAY:
            if (self.visit(node.range_.left) not in [INTNUM, UNKNOWN_TERM] 
                    or self.visit(node.range_.right) not in [INTNUM, UNKNOWN_TERM]):
                self.print_err(node, "Range left and right must be INTNUM")
                return None

            if isinstance(arr.value, ArrayRange):
                return UNKNOWN_ARRAY
            if isinstance(node.range_.left, Intnum) and node.range_.left.term >= len(arr.value.values):
                self.print_err(node, f"Index out of range")
                return None
            elif isinstance(node.range_.right, Intnum) and node.range_.right.term > len(arr.value.values):
                self.print_err(node, f"Index out of range")
                return None
            elif isinstance(node.range_.left, Intnum) and isinstance(node.range_.right, Intnum):
                return self.visit(Array(arr.value.values[node.range_.left.term : node.range_.right.term]))
            else:
                return UNKNOWN_ARRAY
        elif arr.type == UNKNOWN_ARRAY:
            return UNKNOWN_ARRAY
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
                if len(node.left.indices.values) != 1:
                    self.print_err(node, "Wrong indexes number for ARRAY")
                    return None
                    
                if self.visit(node.left.indices.values[0]) != INTNUM:
                    self.print_err(node, "Index must be an integer")
                    return None

                if not isinstance(node.left.indices.values[0], Intnum):
                    return UNKNOWN_TERM

                arr = l_symbol.value
                index = node.left.indices.values[0].term
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
                if len(node.left.indices.values) != 2:
                    self.print_err(node, "Wrong indexes number for MATRIX")
                    return None

                if (self.visit(node.left.indices.values[0]) != INTNUM or 
                        self.visit(node.left.indices.values[1]) != INTNUM):
                    self.print_err(node, "Index must be INTNUM")
                    return None

                mat = l_symbol.value

                return_unknown = False
                if not isinstance(node.left.indices.values[0], Intnum):
                    return_unknown = True
                else:
                    row_i = node.left.indices.values[0].term
                    if row_i < 0 or row_i >= len(mat.values):
                        self.print_err(node, "Index out of range")
                        return None

                if not isinstance(node.left.indices.values[1], Intnum):
                    return_unknown = True
                else:
                    col_j = node.left.indices.values[1].term
                    if col_j < 0 or col_j >= len(mat.values[0].values):
                        self.print_err(node, "Index out of range")
                        return None

                if return_unknown:
                    return UNKNOWN_TERM

                if node.op == "=":
                    mat.values[row_i].values[col_j] = node.right
                    return r_type
                else:
                    final_type = ttype[node.op][self.visit(mat.values[row_i].values[col_j])][r_type]
                    if final_type is None:
                        self.print_err(node, f"Incompatible types")
                    return final_type

        else:
            self.print_err(node, "Wrong lvalue type")
            return None

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

        previous_scope = self.scope
        self.scope = "inside_loop"
        self.visit(node.instructions)
        self.scope = previous_scope
    
    def visit_For(self, node):
        type_range = self.visit(node.range_)
        if type_range != RANGE:
            self.print_err(node, f"For range is invalid")
        else:
            self.symbol_table.put(
                node.ref.ref,
                VariableSymbol(node.ref.ref, INTNUM)
            )

        previous_scope = self.scope
        self.scope = "inside_loop"
        self.visit(node.instructions)
        self.scope = previous_scope
        
    def visit_Return(self, node):
        self.visit(node.value)

    def visit_Print(self, node):
        self.visit(node.value)

    def visit_PrintArray(self, node):
        for nd in node.values:
            self.visit(nd)
        return ARRAY

    def visit_Break(self, node):
        if self.scope == 'outside_loop':
            self.print_err(node, 'BREAK outside loop')
    
    def visit_Continue(self, node):
        if self.scope == 'outside_loop':
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