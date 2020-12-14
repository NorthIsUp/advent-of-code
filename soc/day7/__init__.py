from __future__ import annotations
from os import walk
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast, ClassVar
from soc.problem import Problem
from itertools import count
from functools import reduce
from dataclasses import dataclass, field
import re
from pprint import pprint
BagKind = str

@dataclass
class Bag:
    kind: BagKind
    allows: Dict[BagKind, int]
    lineno: int

    G: ClassVar[Dict[BagKind, 'Bag']] = {}

    def __post_init__(self):
        assert self.kind not in self.G, f'{self.kind} already registered. {self}, {self.G.get(self.kind)}'
        self.G[self.kind] = self

    def __repr__(self):
        return f'"{self.kind}"'

    def walk(self, start=0) -> int:
        return sum(
            self.G[bag_kind].walk(start=1) * inside
            for bag_kind, inside in self.allows.items()
        ) + start



class App(Problem):
    lineno = 0
    def transformer(self, line: str) -> Optional[Bag]:
        if not line:
            return

        self.lineno += 1

        # shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        # dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        # vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        # faded blue bags contain no other bags.
        # dotted black bags contain no other bags.

        kind, rules_str = line.split('bags contain')
        rules = [r.strip(' .') for r in rules_str.split(',')]
        allows = {
            rule[2:].replace(' bags', '').replace(' bag', ''): int(rule[0])
            for rule in rules
            if rule[0].isdigit()
        }

        return Bag(
            kind=kind.strip(),
            allows=allows,
            lineno=self.lineno
        )

    def run(self):
        self.load_input()
        
        print(Bag.G['shiny gold'].walk())

        # for bag in self:
        #     walked = [(kind, i) for (kind, i) in Bag.walk(bag.kind)]
        #     if walked:
        #         bags, counts = zip(*walked)
        #         if 'shiny gold' in bags:
        #             print(sum(counts))
        #             print(bags)
                
        # for bp in self:
        #     print(f'{bp.row} {bp.side}: row: {bp.row_number}, col: {bp.column_number}, id: {bp.id}')
