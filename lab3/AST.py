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
class FinishedStruct:
    instructions: Any

@dataclass
class Term:
    term: Any

@dataclass
class Group:
    value: Any

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
class UnLeftExpr:
    op: Any
    right: Any

@dataclass
class UnRightExpr:
    op: Any
    left: Any

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
    range_from: Any
    range_to: Any
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
class ArrayInterior:
    values: Any

@dataclass
class Array:
    interior: Any
