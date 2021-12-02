from __future__ import annotations
import functools

import re
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations, count
from os import walk
from pprint import pprint
from typing import (
    Any,
    ClassVar,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

from soc.problem import Problem


@dataclass(order=True, unsafe_hash=True)
class Joltage:
    jolts: int = field(repr=True)
    lineno: int = field(repr=False, hash=False, compare=False)
    i: int = field(repr=True, hash=False, compare=False)
    
    @property
    def max_out(self) -> int:
        return self.jolts + 3


class App(Problem):
    lineno = 0

    def add_arguments(self):
        """add any args here"""

    def __post_init__(self) -> None:
        """cleanup here"""

    def transformer(self, line: str) -> Optional[Joltage]:
        self.lineno += 1

        if not line:
            return None
        value = int(line.strip())

        return Joltage(value, lineno=self.lineno, i=0)

    @functools.lru_cache(maxsize=None)
    def solve(self, j: Joltage) -> int:
        count = 0
        for n in self.loaded_input[j.i+1:j.i+4]:
            if n.jolts in [j.jolts + 1, j.jolts + 2 ,j.jolts + 3]:
                if n == self.loaded_input[-1]:
                    count += 1
                else:
                    count += self.solve(n)

        return count


    def run(self):
        self.load_input()
        self.loaded_input.append(Joltage(0, 0, 0))
        self.loaded_input = sorted(self.loaded_input)

        loaded_count = len(self.loaded_input)

        diffs = {1:0, 2:0, 3:1}

        print('-' * 10)

        for i, j in enumerate(self.loaded_input):
            j.i = i
            print(j)

            if i + 1 == loaded_count:
                continue

            n = self.loaded_input[i + 1]
            diffs[n.jolts - j.jolts] += 1

        print(diffs)
        print(diffs[1] * diffs[3])

        result = self.solve(self.loaded_input[0])
        # pprint(result)

        print('combos (19208)', result)
