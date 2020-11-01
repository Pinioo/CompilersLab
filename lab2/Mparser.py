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
    """start : struct
             | start struct
             | '{' start '}'
             | start '{' start '}'"""

def p_struct(p):
    """struct : expr ';'
              | cond_expr
              | instruction"""

######################################

def p_expr_const(p):
    """expr : INTNUM
            | FLOATNUM
            | STRING"""
    
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
    """array_interior : array_interior ',' expr
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

def p_cond_expr(p):
    """cond_expr : cond_if
                 | cond_while
                 | cond_for"""

def p_cond_block(p):
    """cond_block : struct
                  | '{' start '}'"""

def p_cond_if(p):
    """cond_if : IF '(' expr ')' cond_block
               | cond_if ELSE cond_block"""

def p_cond_while(p):
    """cond_while : WHILE '(' expr ')' cond_block"""

def p_cond_for(p):
    """cond_for : FOR ID '=' expr ':' expr cond_block"""

#######################################

def p_instruction(p):
    """instruction : BREAK ';'
                   | CONTINUE ';'
                   | RETURN expr ';'
                   | PRINT array_interior ';'"""

#######################################

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()