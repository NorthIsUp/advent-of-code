from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import reduce, total_ordering
from itertools import combinations, count
from os import walk
from pprint import pprint
from typing import (Any, ClassVar, Dict, Generator, Iterable, List, Optional,
                    Tuple, Union, cast)

from aoc_2021.problem import Problem


@dataclass(order=True)
class TheInput:
    value: int = field(compare=True)
    lineno: int = field(compare=False)
    """make this the input class"""

    def __repr__(self) -> str:
        return f'{self.value}'

    def __add__(self, other: Union[int, TheInput]) -> int:
        if isinstance(other, TheInput):
            other = other.value
        return self.value + other
    __radd__ = __add__

assert TheInput(3, 100) < TheInput(4, 0)


class App(Problem[TheInput]):
    lineno = 0

    def add_arguments(self):
        """add any args here"""

    def __post_init__(self) -> None:
        """cleanup here"""

    def transformer(self, line: str) -> Optional[TheInput]:
        self.lineno += 1

        if not line:
            return None
        value = int(line.strip())

        return TheInput(value, lineno=self.lineno)

    def run(self):
        self.load_input()

        p = None
        i = 0
        windows = zip(
            self.input_windows(size=3, start=0, step=1),
            self.input_windows(size=3, start=1, step=1)
        )
        for x, y in windows:
            print("x", x, sum(x))
            print("y", y, sum(y))
            if sum(x) < sum(y):
                i +=1

        # for x, y in zip([_.value for _ in self] + [0], [0] + [_.value for _ in self]):
        #     i += x > y
        
        print(i)
        # previous: int = self[0].value
        # for v in self[1:]:
        #     print(v)
        #     if v.value > previous:
        #         i += 1
        #     previous = v.value

        # print(sum([1 for i, v in enumerate(self[1:]) if v.value > self[i - 1].value]))
