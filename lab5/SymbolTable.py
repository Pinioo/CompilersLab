class VariableSymbol():
    def __init__(self, name, ttype, value=None):
        self.name = name
        self.type = ttype
        self.value = value

class SymbolTable(object):
    def __init__(self, parent, name): # parent scope and symbol table name
        self.symbols = {}
        self.parent = parent
        self.name = name

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None

    def create_child_scope(self, name):
        return SymbolTable(self, name)