from inspect import cleandoc
problem_template = cleandoc('''
from __future__ import annotations

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


@dataclass
class TheInput:
    lineno: int
    """make this the input class"""


class App(Problem):
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

        for some_input in self:
            pass

''')
