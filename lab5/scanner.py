import ply.lex as lex

reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    "eye": "EYE",
    "zeros": "ZEROS",
    "ones": "ONES",
    "print": "PRINT"
}

tokens = ["FLOATNUM", "INTNUM", "ID",
        "MPLUS", "MMINUS", "MDIV", "MMLTP",
        "PLUSASSIGN", "MINASSIGN", "MULTASSIGN", "DIVASSIGN",
        "GTEQ", "LTEQ", "NEQ", "EQ",
        "STRING"
        ] + list(reserved.values())

t_MPLUS = r"\.\+"
t_MMINUS = r"\.-"
t_MMLTP = r"\.\*"
t_MDIV = r"\./"

t_PLUSASSIGN = r"\+="
t_MINASSIGN = r"-="
t_MULTASSIGN = r"\*="
t_DIVASSIGN = r"/="

t_GTEQ = ">="
t_LTEQ = "<="
t_NEQ = "!="
t_EQ = "=="

literals = r"+-/*=<>()[]{}:',;"

def t_FLOATNUM(t):
    r'( (0 | ([1-9]\d*) )\.\d*) | (\.\d+)'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'([1-9]\d*)|0'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][\w_]*'
    t.type = reserved.get(t.value, "ID")
    return t

def t_STRING(t):
    r'"([^"\\] | (\\.))*"'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_comment(t):
    r'\#.*'

def t_error(t):
    print(f"({t.lexer.lineno}): Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
