import ply.lex as lex

literals = r"+-/*=<>()[]{}:',;"

reserved = {
    "if": "IF",
    "else": "ELSE",
    "then": "THEN",
    "while": "WHILE",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    "eye": "EYE",
    "zeros": "ZEROS",
    "ones": "ONES",
    "print": "PRINT"
}

tokens = ["FLOATNUM", "INTNUM", "ID",
        "BINPLUS", "BINMINUS", "BINDIV", "BINMLTP",
        "PLUSASSIGN", "MINASSIGN", "MULTASSIGN", "DIVASSIGN",
        "GTEQ", "LTEQ", "NEQ", "EQ",
        "STRING"
        ] + list(reserved.values())

t_BINPLUS = r"\.\+"
t_BINMINUS = r"\.-"
t_BINMLTP = r"\.\*"
t_BINDIV = r"\./"

t_PLUSASSIGN = r"\+="
t_MINASSIGN = r"-="
t_MULTASSIGN = r"\*="
t_DIVASSIGN = r"/="

t_GTEQ = "<="
t_LTEQ = ">="
t_NEQ = "!="
t_EQ = "=="

def t_FLOATNUM(t):
    # 10.1 9. 
    r'-?( ( (0 | ([1-9]\d*) )\.\d*) | (\.\d+) )'
    return t

def t_INTNUM(t):
    r'-?([1-9]\d*)|0'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][\w_]*'
    t.type = reserved.get(t.value, "ID")
    return t

def t_STRING(t):
    r'"([^"\\] | (\\.))*"'
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

class Scanner:
    def build(self):
        self.lexer = lex.lex()

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()