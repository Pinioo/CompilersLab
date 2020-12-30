class Memory:
    def __init__(self, name): # memory name
        self.name = name
        self.value_table = {}

    def has_key(self, name):  # variable name
        return name in self.value_table

    def get(self, name):         # gets from memory current value of variable <name>
        return self.value_table[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.value_table[name] = value

class MemoryStack:                                                
    def __init__(self, memory = Memory("program")): # initialize memory stack with memory <memory>
        self.memories = [memory]

    def get(self, name):             # gets from memory stack current value of variable <name>
        for mem in self.memories[::-1]:
            if mem.has_key(name):
                return mem.get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memories[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for mem in self.memories[::-1]:
            if mem.has_key(name):
                mem.put(name, value)
                return None
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memories.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.memories.pop()
