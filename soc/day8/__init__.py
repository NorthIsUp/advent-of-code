from __future__ import annotations
from os import walk
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast, ClassVar
from soc.problem import Problem
from itertools import count
from functools import reduce
from dataclasses import dataclass, field
import re
from pprint import pprint

@dataclass
class Instruction:
    kind: str
    value: int
    index: int

    def __post_init__(self):
        assert self.kind in ['acc', 'jmp', 'nop']

    def __repr__(self):
        return f'I({self.index}, "{self.kind}", {self.value})'

    def action(self, as_nop=False):
        if as_nop or self.kind == 'nop':
            return (0, 1 + self.index)
        elif self.kind == 'jmp':
            return (0, self.value + self.index)
        if self.kind == 'acc':
            return (self.value, 1 + self.index)

class App(Problem):
    lineno = 0
    def transformer(self, line: str) -> Optional[Instruction]:
        if not line:
            return None
        self.lineno += 1
        kind, value = line.split()
        return Instruction(kind=kind, value=int(value), index=self.lineno-1)

    def run(self):
        self.load_input()
        tape = self.loaded_input
        
        for j in tape:
            visited = set()
            acc, jump = 0, 0
            if j.kind != 'jmp':
                continue
            else:
                print(f'checking {j} as nop')

            try:
                while True:
                    i = tape[jump]
                    if i.index in visited:
                        raise StopIteration
                    visited.add(i.index)
                    
                    to_add, jump = i.action(as_nop=True) if i == j else i.action()
                    acc += to_add
            except StopIteration:
                print('double execution error')
                continue
            except IndexError:
                print('terminates!')
                print(acc)
                break
