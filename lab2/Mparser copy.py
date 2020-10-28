import scanner
import ply.yacc as yacc
import numpy as np

tokens = scanner.tokens

symtab = {}

precedence = (
   ('left', '=', 'PLUSASSIGN', 'MINASSIGN', 'MULTASSIGN', 'DIVASSIGN'),
   ("left", '+', '-', 'MPLUS', 'MMINUS'),
   ("left", '*', '/', 'MMLTP', 'MDIV'),
   ("right", '-')
#    ("left", '\'')
)


def p_start(p):
    """start : expr ';'
             | start expr ';'"""
    if len(p) == 2:
        print('p[1] =', p[1])
    else:
        print('p[2] =', p[2])

######################################

# def p_term_num(p):
#     """term : INTNUM 
#             | FLOATNUM"""
#     p[0] = p[1]

# def p_term_id(p):
#     """term : ID
#             | ID \"'\""""
#     if p[1] not in symtab:
#         symtab[p[1]] = 0
#         print(f"{p[1]} not used, set to 0")
#     p[0] = symtab[p[1]]

# def p_expr_term(p):
#     """expr : term"""
#     p[0] = p[1]

def p_expr_num(p):
    """expr : INTNUM
            | FLOATNUM"""
    # p[0] = p[1]
    
def p_expr_id(p):
    """expr     : ID
       mat_expr : ID"""  
    # if p[1] in symtab:
    #     p[0] = symtab[p[1]]
    # else:
    #     print(f"{p[1]} probably not assigned a value")

def p_expr_group(p):
    """expr : '(' expr ')'"""
    # p[0] = p[2]

#######################################

def p_expr_negative(p):
    """expr : '-' expr"""
    # p[0] = -p[2]

def p_expr_assign(p):
    """expr     : ID '=' expr
                | ID PLUSASSIGN expr
                | ID MINASSIGN expr
                | ID MULTASSIGN expr
                | ID DIVASSIGN expr
       mat_expr : ID '=' mat_expr"""
    # if p[2] == '=':    symtab[p[1]] = p[3]
    # elif p[2] == '+=': symtab[p[1]] += p[3]
    # elif p[2] == '-=': symtab[p[1]] -= p[3]
    # elif p[2] == '*=': symtab[p[1]] *= p[3]
    # elif p[2] == '/=': symtab[p[1]] /= p[3]
    # p[0] = symtab[p[1]]

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    # if p[2] == '+':     p[0] = p[1] + p[3]
    # elif p[2] == '-':   p[0] = p[1] - p[3]
    # elif p[2] == '*':   p[0] = p[1] * p[3]
    # elif p[2] == '/':   p[0] = p[1] / p[3]

def p_expr_logic(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GTEQ expr
            | expr LTEQ expr
            | expr '>' expr
            | expr '<' expr"""
    # if p[2] == '==':    p[0] = p[1] == p[3]
    # elif p[2] == '!=':  p[0] = p[1] != p[3]
    # elif p[2] == '>=':  p[0] = p[1] >= p[3]
    # elif p[2] == '<=':  p[0] = p[1] <= p[3]
    # elif p[2] == '>':   p[0] = p[1] > p[3]
    # elif p[2] == '<':   p[0] = p[1] < p[3]


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        # print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")

# to finish the grammar
# ....


    


parser = yacc.yacc()