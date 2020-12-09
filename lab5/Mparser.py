import scanner
from AST import *
import ply.yacc as yacc
import numpy as np

tokens = scanner.tokens

symtab = {}

precedence = (
    ("nonassoc", 'SINGLE_IF'),
    ("nonassoc", 'ELSE'),

    ("right", '=', 'PLUSASSIGN', 'MINASSIGN', 'MULTASSIGN', 'DIVASSIGN'),
    ("nonassoc", 'EQ', 'NEQ', '<', '>', 'GTEQ', 'LTEQ'),

    ("left", '+', '-', 'MPLUS', 'MMINUS'),
    ("left", '*', '/', 'MMLTP', 'MDIV'),
    ("right", 'UMINUS'),
    ("left", '\'')
)
    
def p_start(p):
    """start : struct
             | start struct""" 
    if len(p) == 2:
        p[0] = Start([p[1]])
    elif len(p) == 3:
        p[0] = Start(p[1].instructions + [p[2]])
    p[0].line = p.lineno(0)

def p_block(p):
    """block : '{' block_interior '}'"""
    p[0] = p[2]
    p[0].line = p.lineno(0)

def p_struct(p):
    """struct : expr ';'
              | instruction ';'
              | cond_expr
              | block"""
    p[0] = p[1]
    p[0].line = p.lineno(0)

def p_for_struct(p):
    """for_struct : assignment ';'
                  | instruction ';'
                  | cond_expr
                  | block"""
    p[0] = p[1]
    p[0].line = p.lineno(0)

def p_block_interior(p):
    """block_interior : struct
                      | block_interior struct"""
    if len(p) == 2:
        p[0] = Start([p[1]])
    elif len(p) == 3:
        p[0] = Start(p[1].instructions + [p[2]])
    p[0].line = p.lineno(0)

######################################

def p_expr_intnum(p):
    """expr : INTNUM"""
    p[0] = Intnum(p[1])
    p[0].line = p.lineno(0)

def p_expr_floatnum(p):
    """expr : FLOATNUM"""
    p[0] = Floatnum(p[1])
    p[0].line = p.lineno(0)

def p_expr_string(p):
    """expr : STRING"""
    p[0] = String(p[1])
    p[0].line = p.lineno(0)

def p_expr_matfun_zeros(p):
    """expr : ZEROS '(' expr ')'
            | ZEROS '(' expr ',' expr ')'"""
    if len(p) == 5:
        p[0] = Zeros(p[3], p[3])
    else:
        p[0] = Zeros(p[3], p[5])
    p[0].line = p.lineno(0)

def p_expr_matfun_ones(p):
    """expr : ONES '(' expr ')'
            | ONES '(' expr ',' expr ')'"""
    if len(p) == 5:
        p[0] = Ones(p[3], p[3])
    else:
        p[0] = Ones(p[3], p[5])
    p[0].line = p.lineno(0)

def p_expr_matfun_eye(p):
    """expr : EYE '(' expr ')'
            | EYE '(' expr ',' expr ')'"""
    if len(p) == 5:
        p[0] = Eye(p[3], p[3])
    else:
        p[0] = Eye(p[3], p[5])
    p[0].line = p.lineno(0)
    
def p_expr_lvalue(p):
    """expr : lvalue"""
    p[0] = p[1]
    p[0].line = p.lineno(0)

def p_expr_group(p):
    """expr : '(' expr ')'"""
    p[0] = p[2]
    p[0].line = p.lineno(0)

#######################################

def p_expr_unmin(p):
    """expr : '-' expr %prec UMINUS"""
    p[0] = UnOp(p[1], p[2])
    p[0].line = p.lineno(0)

def p_expr_transpose(p):
    """expr : expr '\\\''"""    
    p[0] = UnOp(p[2], p[1])
    p[0].line = p.lineno(0)

#######################################

def p_array_interior_unfinished(p):
    """array_interior : array_interior ',' expr"""
    p[0] = Array(p[1].values + [p[3]])
    p[0].line = p.lineno(0)

def p_array_interior_finished(p):
    """array_interior : expr"""
    p[0] = Array([p[1]])
    p[0].line = p.lineno(0)

def p_range(p):
    """range : expr ':' expr"""
    p[0] = Range(p[1], p[3])
    p[0].line = p.lineno(0)

def p_expr_array(p):
    """expr : '[' array_interior ']'"""
    p[0] = p[2]
    p[0].line = p.lineno(0)

def p_expr_empty_array(p):
    """expr : '[' ']'"""
    p[0] = Array([])
    p[0].line = p.lineno(0)

#######################################

def p_lvalue_single(p):
    """lvalue : ID"""
    p[0] = Id(p[1])
    p[0].line = p.lineno(0)

def p_lvalue_ref_indices(p):
    """lvalue : ID '[' array_interior ']'"""
    p[0] = ArrayRef(p[1], p[3])
    p[0].line = p.lineno(0)

def p_lvalue_ref_range(p):
    """lvalue : ID '[' range ']'"""
    p[0] = ArrayRange(p[1], p[3])
    p[0].line = p.lineno(0)

def p_assign(p):
    """assignment : lvalue '=' expr
                  | lvalue PLUSASSIGN expr
                  | lvalue MINASSIGN expr
                  | lvalue MULTASSIGN expr
                  | lvalue DIVASSIGN expr"""
    p[0] = Assign(p[2], p[1], p[3])
    p[0].line = p.lineno(0)

def p_expr_assign(p):
    """expr : assignment"""
    p[0] = p[1]
    p[0].line = p.lineno(0)

#######################################

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    p[0] = BinOp(p[2], p[1], p[3])
    p[0].line = p.lineno(0)

def p_expr_matop(p):
    """expr : expr MPLUS expr
            | expr MMINUS expr
            | expr MMLTP expr
            | expr MDIV expr"""
    p[0] = BinOp(p[2], p[1], p[3])
    p[0].line = p.lineno(0)

#######################################

def p_expr_logic(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GTEQ expr
            | expr LTEQ expr
            | expr '>' expr
            | expr '<' expr"""
    p[0] = BinOp(p[2], p[1], p[3])
    p[0].line = p.lineno(0)

#######################################

def p_cond_expr(p):
    """cond_expr : cond_if
                 | cond_while
                 | cond_for"""
    p[0] = p[1]
    p[0].line = p.lineno(0)

def p_cond_if(p):
    """cond_if : IF '(' expr ')' struct %prec SINGLE_IF"""
    p[0] = If(p[3], p[5])
    p[0].line = p.lineno(0)

def p_cond_if_else(p):
    """cond_if : IF '(' expr ')' struct ELSE struct"""
    p[0] = IfElse(p[3], p[5], p[7])
    p[0].line = p.lineno(0)

#######################################

def p_cond_while(p):
    """cond_while : WHILE '(' expr ')' struct"""
    p[0] = While(p[3], p[5])
    p[0].line = p.lineno(0)

def p_cond_for(p):
    """cond_for : FOR lvalue '=' range for_struct"""
    p[0] = For(p[2], p[4], p[5])
    p[0].line = p.lineno(0)

#######################################

def p_instruction_return(p):
    """instruction : RETURN expr"""
    p[0] = Return(p[2])
    p[0].line = p.lineno(0)

def p_instruction_print(p):
    """instruction : PRINT array_interior"""
    p[0] = Print(p[2])
    p[0].line = p.lineno(0)

def p_instruction_break(p):
    """instruction : BREAK"""
    p[0] = Break()
    p[0].line = p.lineno(0)

def p_instruction_continue(p):
    """instruction : CONTINUE"""
    p[0] = Continue()
    p[0].line = p.lineno(0)

#######################################

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()