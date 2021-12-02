from __future__ import annotations

import re
import sys
from argparse import ArgumentParser
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations, count
from operator import add, mul, sub
from pprint import pprint
from typing import *  # type: ignore

from aoc_2021.problem import Problem

try:
    from rich import inspect, pretty, print, traceback
    from rich.console import Console
except ImportError:
    print('rich not loaded', file=sys.stderr)
else:
    traceback.install(show_locals=0)
    console = Console()
    pretty.install()

@dataclass(order=True)
class TheInput:
    """make this the input class"""
    lineno: int = field(compare=False)
    value: int = field(compare=True)

    def __math__(self, op: Callable[[TheInput, Union[int, TheInput]], int], other: Union[int, TheInput]) -> int:
        if isinstance(other, TheInput):
            other = other.value
        return op(self, other)

    def __add__(self, other: Union[int, TheInput]) -> int:
        return self.__math__(add, other)

    def __sub__(self, other: Union[int, TheInput]) -> int:
        return self.__math__(sub, other)

    def __mul__(self, other: Union[int, TheInput]) -> int:
        return self.__math__(mul, other)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__

class App(Problem[TheInput]):
    lineno = 0

    def add_arguments(self, parser: ArgumentParser):
        """add any args here"""

    def __post_init__(self) -> None:
        """cleanup here"""
        super().__post_init__()

    def transformer(self, line: str) -> Optional[TheInput]:
        self.lineno += 1

        if not line:
            return None

        value = int(line.strip())

        return TheInput(
            value=value,
            lineno=self.lineno,
        )

    def run(self):
        self.load_input()

        # part 1
        for x in self:
            pass

        print(f'part 1 results:')

        # part 2
        print(f'part 1 results:')
