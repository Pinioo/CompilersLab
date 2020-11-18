import scanner
import AST
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

def p_struct(p):
    """struct : single_stmt ';'
              | cond_expr
              | '{' block_interior '}'"""

def p_block_interior(p):
    """block_interior : block_interior expr ';'
                      | block_interior instruction ';'
                      | expr ';'
                      | instruction ';'"""

def p_single_statement(p):
    """single_stmt : instruction
                   | assignment"""

######################################

def p_loop_struct(p):
    """loop_struct : loop_single_stmt ';'
                   | loop_cond_expr
                   | '{' loop_block_interior '}'"""

def p_loop_block_interior(p):
    """loop_block_interior : loop_block_interior expr ';'
                           | loop_block_interior loop_instruction ';'
                           | loop_block_interior loop_cond_expr
                           | expr ';'
                           | loop_instruction ';'
                           | loop_cond_expr"""

def p_loop_single_statement(p):
    """loop_single_stmt : loop_instruction
                        | assignment"""

######################################

def p_expr_const(p):
    """expr : INTNUM
            | FLOATNUM
            | STRING"""
    p[0] = AST.Term(p[1])

def p_expr_matfun(p):
    """expr : ZEROS '(' expr ')'
            | ONES '(' expr ')'
            | EYE '(' expr ')'"""
    
def p_expr_lvalue(p):
    """expr : lvalue"""
    # p[0] = AST.Term(p[1])

def p_expr_group(p):
    """expr : '(' expr ')'"""

#######################################

def p_expr_unmin(p):
    """expr : '-' expr %prec UMINUS"""
    p[0] = AST.UnRightExpr(p[0], p[1])

def p_expr_transpose(p):
    """expr : expr '\\\''"""    
    p[0] = AST.UnLeftExpr(p[1], p[0])

#######################################

def p_array_interior(p):
    """array_interior : array_interior ',' expr
                      | expr"""
    
def p_expr_array(p):
    """expr : '[' array_interior ']'"""

#######################################

def p_lvalue(p):
    """lvalue : ID
              | ID '[' array_interior ']'"""

def p_assign(p):
    """assignment : lvalue '=' expr
                  | lvalue PLUSASSIGN expr
                  | lvalue MINASSIGN expr
                  | lvalue MULTASSIGN expr
                  | lvalue DIVASSIGN expr"""
    
def p_expr_assign(p):
    """expr : assignment"""

#######################################

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])

def p_expr_matop(p):
    """expr : expr MPLUS expr
            | expr MMINUS expr
            | expr MMLTP expr
            | expr MDIV expr"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])

#######################################

def p_expr_logic(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GTEQ expr
            | expr LTEQ expr
            | expr '>' expr
            | expr '<' expr"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])

#######################################

def p_cond_expr(p):
    """cond_expr : cond_if
                 | cond_while
                 | cond_for"""

def p_cond_block(p):
    """cond_block : struct"""

def p_cond_if(p):
    """cond_if : IF '(' expr ')' cond_block %prec SINGLE_IF
               | IF '(' expr ')' cond_block ELSE cond_block"""

#######################################

def p_loop_cond_expr(p):
    """loop_cond_expr : loop_cond_if
                      | cond_while
                      | cond_for"""

def p_loop_cond_block(p):
    """loop_cond_block : loop_struct"""

def p_loop_cond_if(p):
    """loop_cond_if : IF '(' expr ')' loop_cond_block %prec SINGLE_IF
                    | IF '(' expr ')' loop_cond_block ELSE loop_cond_block"""

def p_cond_while(p):
    """cond_while : WHILE '(' expr ')' loop_cond_block"""

def p_cond_for(p):
    """cond_for : FOR ID '=' expr ':' expr loop_cond_block"""

#######################################

def p_instruction(p):
    """instruction : RETURN expr
                   | PRINT array_interior"""

def p_loop_instruction(p):
    """loop_instruction : BREAK
                        | CONTINUE
                        | RETURN expr
                        | PRINT array_interior"""

#######################################

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()