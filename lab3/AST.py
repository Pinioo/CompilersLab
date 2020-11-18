from dataclasses import dataclass
from typing import Any

@dataclass
class Program:
    instructions: Any

@dataclass
class Block:
    instructions: Any

@dataclass
class Term:
    term: Any

@dataclass
class Id:
    id: Any

@dataclass
class ArrayRef:
    id: Any
    indices: Any 

@dataclass
class BinExpr:
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
    id: Any
    range_from: Any
    range_to: Any
    instructions: Any

@dataclass
class Return:
    value: Any

@dataclass
class Break:
    pass

@dataclass
class Continue:
    pass

@dataclass
class Matfun:
    name: Any
    argument: Any

@dataclass
class ArrayInterior:
    pass

@dataclass
class Array:
    interior: Any
