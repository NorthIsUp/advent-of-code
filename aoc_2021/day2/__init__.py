from __future__ import annotations

import re
from argparse import ArgumentParser
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
    Literal,
    Optional,
    Tuple,
    Union,
    cast,
)

from click import Argument

from aoc_2021.problem import Problem


@dataclass
class TheInput:
    lineno: int
    direction: Literal['up', 'down', 'forward']
    value: int
    """make this the input class"""


class App(Problem):
    lineno = 0

    def __post_init__(self) -> None:
        """cleanup here"""
        super().__post_init__()

    def transformer(self, line: str) -> Optional[TheInput]:
        self.lineno += 1

        if not line:
            return None
        direction, value = line.split()

        return TheInput(direction=direction, value=int(value), lineno=self.lineno)

    def run(self):
        self.load_input()

        depth = 0
        horozontal = 0
        aim = 0
        for x in self:
            if x.direction == 'up':
                aim -= x.value
            if x.direction == 'down':
                aim += x.value
            if x.direction == 'forward':
                horozontal += x.value
                depth += x.value * aim
                print(x.value, aim, x.value * aim)

        print(depth, horozontal, depth * horozontal)
