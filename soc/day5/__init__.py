from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast
from soc.problem import Problem
from itertools import count
from functools import reduce
from dataclasses import dataclass, field
import re
from pprint import pprint



@dataclass
class BoardingPass:
    row: str
    side: str
    lineno: int

    @property
    def row_number(self) -> int:
        return self.binary(self.row, 'F', 127)

    @property
    def column_number(self) -> int:
        return self.binary(self.side, 'L', 7)

    @property
    def id(self) -> int:
        return self.row_number * 8 + self.column_number

    def binary(self, s, p, hi) -> int:
        lo = 0
        for pivot in s:
            half = (lo + hi) // 2
            lo, hi = (lo, half) if pivot == p else (half, hi)
            # print(pivot, lo, hi)
        return hi


    def __repr__(self) -> str:
        s = self
        return f'BoardingPass({s.row} {s.side}: row: {s.row_number}, col: {s.column_number}, id: {s.id})'

class App(Problem):
    lineno = 0
    def transformer(self, line: str) -> Optional[BoardingPass]:
        if not line:
            return
        self.lineno += 1
        return BoardingPass(
            lineno=self.lineno,
            row=line[:7],
            side=line[7:]
        )

    def run(self):
        print(max(bp.id for bp in self))
        passes = sorted(self, key=lambda bp: bp.id)

        for i, p in enumerate(passes[1:-1], 1):
            if passes[i-1].id +1 != p.id:
                for p in passes[i-2: i+2]:
                    print(p)

        # for bp in self:
        #     print(f'{bp.row} {bp.side}: row: {bp.row_number}, col: {bp.column_number}, id: {bp.id}')
