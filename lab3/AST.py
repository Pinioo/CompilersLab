from dataclasses import dataclass
from typing import Any

@dataclass
class Term:
    term: Any

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