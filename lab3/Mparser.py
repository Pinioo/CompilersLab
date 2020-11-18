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

def p_root(p):
    """root : start"""
    p[0] = Root(p[1])
    
def p_start(p):
    """start : struct
             | start struct""" 
    if len(p) == 2:
        p[0] = Start([p[1]])
    elif len(p) == 3:
        p[0] = Start(p[1].instructions + [p[2]])

def p_block(p):
    """block : '{' block_interior '}'"""
    p[0] = Block(p[2])

def p_struct(p):
    """struct : expr ';'
              | instruction ';'
              | cond_expr
              | block"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = FinishedStruct(p[1])

def p_block_interior(p):
    """block_interior : struct
                      | block_interior struct"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Start(p[1].instructions + [p[2]])
    

######################################

def p_loop_block(p):
    """loop_block : '{' loop_block_interior '}'"""
    p[0] = Block(p[2])

def p_loop_struct(p):
    """loop_struct : loop_single_stmt ';'
                   | loop_cond_expr
                   | loop_block"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = FinishedStruct(p[1])
    

def p_loop_block_interior_continues(p):
    """loop_block_interior : loop_block_interior expr ';'
                           | loop_block_interior loop_instruction ';'
                           | loop_block_interior loop_cond_expr"""
    if p[-1] == ';':
        p[0] = Start(p[1].instructions + [p[2]])
    else:
        p[0] = Start(p[1].instructions + [FinishedStruct(p[2])])
    
def p_loop_block_interior_finish(p):
    """loop_block_interior : expr ';'
                           | loop_instruction ';'
                           | loop_cond_expr"""
    if len(p) == 2:
        p[0] = Start([p[1]])
    elif len(p) == 3:
        p[0] = Start([FinishedStruct(p[1])]) 

def p_loop_single_statement(p):
    """loop_single_stmt : loop_instruction
                        | assignment"""
    p[0] = p[1]

######################################

def p_expr_const(p):
    """expr : INTNUM
            | FLOATNUM
            | STRING"""
    p[0] = Term(p[1])

def p_expr_matfun_zeros(p):
    """expr : ZEROS '(' expr ')'"""
    p[0] = Zeros(p[3])
    
def p_expr_matfun_ones(p):
    """expr : ONES '(' expr ')'"""
    p[0] = Ones(p[3])

def p_expr_matfun_eye(p):
    """expr : EYE '(' expr ')'"""
    p[0] = Eye(p[3])
    
def p_expr_lvalue(p):
    """expr : lvalue"""
    p[0] = p[1]

def p_expr_group(p):
    """expr : '(' expr ')'"""
    p[0] = Group(p[2])

#######################################

def p_expr_unmin(p):
    """expr : '-' expr %prec UMINUS"""
    p[0] = UnLeftExpr(p[1], p[2])

def p_expr_transpose(p):
    """expr : expr '\\\''"""    
    p[0] = UnRightExpr(p[2], p[1])

#######################################

def p_array_interior_unfinished(p):
    """array_interior : array_interior ',' expr"""
    # p[0] = ArrayInterior(p[1], p[3])
    # p[0] = Start(p[1].instructions + [p[3]])
    p[0] = ArrayInterior(p[1].values + [p[3]])

def p_array_interior_finished(p):
    """array_interior : expr"""
    # p[0] = p[1]
    # p[0] = Start([p[1]])
    p[0] = ArrayInterior([p[1]])

def p_expr_array(p):
    """expr : '[' array_interior ']'"""
    p[0] = Array(p[2])

#######################################

def p_lvalue_single(p):
    """lvalue : ID"""
    p[0] = Id(p[1])

def p_lvalue_ref(p):
    """lvalue : ID '[' array_interior ']'"""
    p[0] = ArrayRef(p[1], p[3])

def p_assign(p):
    """assignment : lvalue '=' expr
                  | lvalue PLUSASSIGN expr
                  | lvalue MINASSIGN expr
                  | lvalue MULTASSIGN expr
                  | lvalue DIVASSIGN expr"""
    p[0] = Assign(p[2], p[1], p[3])

def p_expr_assign(p):
    """expr : assignment"""
    p[0] = p[1]

#######################################

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    p[0] = BinOp(p[2], p[1], p[3])

def p_expr_matop(p):
    """expr : expr MPLUS expr
            | expr MMINUS expr
            | expr MMLTP expr
            | expr MDIV expr"""
    p[0] = MatOp(p[2], p[1], p[3])

#######################################

def p_expr_logic(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GTEQ expr
            | expr LTEQ expr
            | expr '>' expr
            | expr '<' expr"""
    p[0] = LogicOp(p[2], p[1], p[3])

#######################################

def p_cond_expr(p):
    """cond_expr : cond_if
                 | cond_while
                 | cond_for"""
    p[0] = p[1]

def p_cond_if(p):
    """cond_if : IF '(' expr ')' struct %prec SINGLE_IF"""
    p[0] = If(p[3], p[5])

def p_cond_if_else(p):
    """cond_if : IF '(' expr ')' struct ELSE struct"""
    p[0] = IfElse(p[3], p[5], p[7])

#######################################

def p_loop_cond_expr(p):
    """loop_cond_expr : loop_cond_if
                      | cond_while
                      | cond_for"""
    p[0] = p[1]

def p_loop_cond_if(p):
    """loop_cond_if : IF '(' expr ')' loop_struct %prec SINGLE_IF"""
    p[0] = If(p[3], p[5])

def p_loop_cond_if_else(p):
    """loop_cond_if : IF '(' expr ')' loop_struct ELSE loop_struct"""
    p[0] = IfElse(p[3], p[5], p[7])

def p_cond_while(p):
    """cond_while : WHILE '(' expr ')' loop_struct"""
    p[0] = While(p[3], p[5])

def p_cond_for(p):
    """cond_for : FOR ID '=' expr ':' expr loop_struct"""
    p[0] = For(p[2], p[4], p[6], p[7])

#######################################

def p_instruction_return(p):
    """instruction : RETURN expr"""
    p[0] = Return(p[2])

def p_instruction_print(p):
    """instruction : PRINT array_interior"""
    p[0] = Print(p[2])

def p_loop_instruction_break(p):
    """loop_instruction : BREAK"""
    p[0] = Break()

def p_loop_instruction_continue(p):
    """loop_instruction : CONTINUE"""
    p[0] = Continue()

def p_loop_instruction(p):
    """loop_instruction : instruction"""
    p[0] = p[1]

#######################################

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()