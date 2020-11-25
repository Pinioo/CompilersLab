from dataclasses import dataclass
from typing import Any

@dataclass
class Root:
    instructions: Any

@dataclass
class Start:
    instructions: Any

@dataclass
class Block:
    instructions: Any

@dataclass
class Struct:
    instructions: Any

@dataclass
class Term:
    term: Any

@dataclass
class Id:
    ref: Any

@dataclass
class ArrayRef:
    ref: Any
    indices: Any 

@dataclass
class Assign:
    op: Any
    left: Any
    right: Any

@dataclass
class BinOp:
    op: Any
    left: Any
    right: Any

@dataclass
class MatOp:
    op: Any
    left: Any
    right: Any

@dataclass
class LogicOp:
    op: Any
    left: Any
    right: Any

@dataclass
class UnOp:
    op: Any
    expr: Any

@dataclass
class If:
    condition: Any
    instructions: Any

@dataclass
class IfElse:
    condition: Any
    if_instructions: Any
    else_instructions: Any

@dataclass
class While:
    condition: Any
    instructions: Any

@dataclass
class For:
    ref: Any
    range_: Any
    instructions: Any

@dataclass
class Return:
    value: Any

@dataclass
class Print:
    value: Any

@dataclass
class Break:
    pass

@dataclass
class Continue:
    pass

@dataclass
class Ones:
    argument: Any

@dataclass
class Zeros:
    argument: Any

@dataclass
class Eye:
    argument: Any

@dataclass
class Array:
    values: Any

@dataclass
class Range:
    left: Any
    right: Any
