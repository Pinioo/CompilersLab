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

def p_loop_start(p):
    """loop_start : loop_struct
                  | loop_start loop_struct
                  | '{' loop_start '}'
                  | loop_start '{' loop_start '}'"""

def p_loop_struct(p):
    """loop_struct : expr ';'
                   | loop_cond_expr
                   | loop_instruction"""

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
    """expr : ID '[' expr ']' '=' expr
            | ID '[' expr ']' PLUSASSIGN expr
            | ID '[' expr ']' MINASSIGN expr
            | ID '[' expr ']' MULTASSIGN expr    
            | ID '[' expr ']' DIVASSIGN expr"""

def p_expr_matassign(p):
    """expr : ID '[' expr ',' expr ']' '=' expr
            | ID '[' expr ',' expr ']' PLUSASSIGN expr
            | ID '[' expr ',' expr ']' MINASSIGN expr
            | ID '[' expr ',' expr ']' MULTASSIGN expr    
            | ID '[' expr ',' expr ']' DIVASSIGN expr"""

def p_expr_matinit_special(p):
    """expr : ID '=' ZEROS '(' expr ')'
            | ID '=' ONES '(' expr ')'
            | ID '=' EYE '(' expr ')'"""

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

#######################################

def p_loop_cond_expr(p):
    """loop_cond_expr : loop_cond_if
                      | cond_while
                      | cond_for"""

def p_loop_cond_block(p):
    """loop_cond_block : loop_struct
                       | '{' loop_start '}'"""

def p_loop_cond_if(p):
    """loop_cond_if : IF '(' expr ')' loop_cond_block
                    | loop_cond_if ELSE loop_cond_block"""

def p_cond_while(p):
    """cond_while : WHILE '(' expr ')' loop_cond_block"""

def p_cond_for(p):
    """cond_for : FOR ID '=' expr ':' expr loop_cond_block"""

#######################################

def p_instruction(p):
    """instruction : RETURN expr ';'
                   | PRINT array_interior ';'"""

def p_loop_instruction(p):
    """loop_instruction : BREAK ';'
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