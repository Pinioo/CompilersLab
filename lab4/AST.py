from dataclasses import dataclass
from typing import Any

class Node:
    def __init__(self):
        self.line = 0

    def accept(self, visitor):
        return visitor.visit(self)

@dataclass
class Start(Node):
    instructions: Any

@dataclass
class Block(Node):
    instructions: Any

@dataclass
class Struct(Node):
    instructions: Any

@dataclass
class Term(Node):
    term: Any

@dataclass
class Id(Node):
    ref: Any

@dataclass
class ArrayRef(Node):
    ref: Any
    indices: Any 

@dataclass
class ArrayRange(Node):
    ref: Any
    range_: Any

@dataclass
class Assign(Node):
    op: Any
    left: Any
    right: Any

@dataclass
class BinOp(Node):
    op: Any
    left: Any
    right: Any

@dataclass
class UnOp(Node):
    op: Any
    expr: Any

@dataclass
class If(Node):
    condition: Any
    instructions: Any

@dataclass
class IfElse(Node):
    condition: Any
    if_instructions: Any
    else_instructions: Any

@dataclass
class While(Node):
    condition: Any
    instructions: Any

@dataclass
class For(Node):
    ref: Any
    range_: Any
    instructions: Any

@dataclass
class Return(Node):
    value: Any

@dataclass
class Print(Node):
    value: Any

@dataclass
class Break(Node):
    pass

@dataclass
class Continue(Node):
    pass

@dataclass
class Ones(Node):
    rows: Any
    columns: Any

@dataclass
class Zeros(Node):
    rows: Any
    columns: Any

@dataclass
class Eye(Node):
    rows: Any
    columns: Any

@dataclass
class Array(Node):
    values: Any

@dataclass
class Range(Node):
    left: Any
    right: Any
