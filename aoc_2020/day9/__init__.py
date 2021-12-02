from __future__ import annotations
from os import walk
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast, ClassVar
from soc.problem import Problem
from itertools import count, combinations
from functools import reduce
from dataclasses import dataclass, field
import re
from pprint import pprint

@dataclass
class Window:
    values: List[int] = field(default_factory=list)
    preamble: int = 25

    def __iter__(self):
        yield from (x + y for x, y in combinations(self.values, 2))

    @property
    def full(self):
        return len(self.values) >= self.preamble

    def push(self, value: int):
        while self.full:
            self.values.pop(0)

        self.values.append(value)

class App(Problem):
    lineno = 0
    window = Window()

    def add_arguments(self):
        self.add_argument('--preamble', type=int, default=25)
    
    def __post_init__(self) -> None:
        self.window.preamble = self.args.preamble

    def transformer(self, line: str) -> Optional[int]:
        if not line:
            return None
        value = int(line.strip())
        
        if not self.window.full:
            self.window.push(value)

        return value

    def run(self):
        self.load_input()
        i = -1
        for i in self.loaded_input[self.args.preamble:]:
            if i not in self.window:
                print('missing', i, list(self.window))
                break
            self.window.push(i)

        for x in range(0, len(self.loaded_input)):
            for y in range(x, len(self.loaded_input)):
                slice = self.loaded_input[x:y]
                if i == sum(slice):
                    hi = max(slice)
                    lo = min(slice)
                    print('weakness', lo, '+', hi, '=',lo+hi)
                    break
            else:
                continue
            break
