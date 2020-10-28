import scanner
import ply.yacc as yacc
import numpy as np

tokens = scanner.tokens

symtab = {}

precedence = (
   ('left', '=', 'PLUSASSIGN', 'MINASSIGN', 'MULTASSIGN', 'DIVASSIGN'),
   ("left", '+', '-', 'MPLUS', 'MMINUS'),
   ("left", '*', '/', 'MMLTP', 'MDIV'),
   ("right", '-'),
   ("left", '\'')
)


def p_start(p):
    """start : expr ';'
             | block 
             | start expr ';'
             | start block"""
    print('start')

######################################

def p_expr_num(p):
    """expr : INTNUM
            | FLOATNUM"""
    
def p_expr_id(p):
    """expr : ID"""

def p_expr_group(p):
    """expr : '(' expr ')'"""

#######################################

def p_expr_unmin(p):
    """expr : '-' expr"""

def p_expr_transpose(p):
    """expr : expr '\\\''"""    

#######################################

def p_array_interior(p):
    """array_interior : expr ',' array_interior
                      | expr"""
    
def p_expr_array(p):
    """expr : '[' array_interior ']'"""

#######################################

def p_expr_assign(p):
    """expr : ID '=' expr
            | ID PLUSASSIGN expr
            | ID MINASSIGN expr
            | ID MULTASSIGN expr
            | ID DIVASSIGN expr"""

def p_expr_arrassign(p):
    """expr : ID '[' INTNUM ']' '=' expr
            | ID '[' INTNUM ']' PLUSASSIGN expr
            | ID '[' INTNUM ']' MINASSIGN expr
            | ID '[' INTNUM ']' MULTASSIGN expr    
            | ID '[' INTNUM ']' DIVASSIGN expr"""

def p_expr_matassign(p):
    """expr : ID '[' INTNUM ',' INTNUM ']' '=' expr
            | ID '[' INTNUM ',' INTNUM ']' PLUSASSIGN expr
            | ID '[' INTNUM ',' INTNUM ']' MINASSIGN expr
            | ID '[' INTNUM ',' INTNUM ']' MULTASSIGN expr    
            | ID '[' INTNUM ',' INTNUM ']' DIVASSIGN expr"""

def p_expr_matinit_special(p):
    """expr : ID '=' ZEROS '(' INTNUM ')'
            | ID '=' ONES '(' INTNUM ')'
            | ID '=' EYE '(' INTNUM ')'"""

#######################################

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""

def p_expr_matop(p):
    """expr : expr MPLUS expr
            | expr MMINUS expr
            | expr MMLTP expr
            | expr MDIV expr"""

#######################################

def p_expr_logic(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GTEQ expr
            | expr LTEQ expr
            | expr '>' expr
            | expr '<' expr"""

#######################################

def p_block(p):
    """block : expr ';'
             | '{' '}'
             | '{' start '}'
             | while_block
             | if_block"""
    print('block')

def p_while_block(p):
    """while_block : WHILE '(' expr ')' block"""
    print('while')

def p_if_block(p):
    """if_block : IF '(' expr ')' block"""

def p_else_block(p):
    """else_block : ELSE block"""

#######################################

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        # print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()