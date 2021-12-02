from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations, count, cycle, permutations, product
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
COORDS = tuple((x, y) for (x,y) in product((-1, 0, 1),(-1, 0, 1)) if (x,y) != (0, 0))
print(COORDS)

@dataclass
class Seats:
    """make this the input class"""
    seats: List[str] = field(default_factory=list)
    rows:int = 0
    cols:int = 0

    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.seats)

    def fmt_before_after(self, before, after):
        out = []
        for b, a in zip(before, after):
            out.append(''.join(b) + '\t->\t' + ''.join(a))
        return '\n'.join(out)

    def append(self, line: str):
        self.seats.append(list(line))
        self.rows = len(self.seats)
        self.cols = len(self.seats[-1])

    def get(self, r: int, c: int) -> str:
        try:
            if r < 0 or c < 0:
                raise IndexError
            return self.seats[r][c]
        except IndexError:
            return ''

    def count_occupied_near(self, row, col, coords=COORDS) -> int:
        incr = 0
        for s in count(1):
            seen = 0
            for i, j in coords:
                if (row == col == 0):
                    print(f'{row}{i*s:+d},{col}{j*s:+d}')
                seat = self.get(row + i * s, col + j * s)
                seen += bool(seat)
                incr += seat == '#'
            if seen == 0:
                break
        return incr
     
    def count_occupied(self) -> int:
        return sum(c == '#' for row in self.seats for c in row)

    def should_occupy(self, r, c) -> str:
        near = self.count_occupied_near(r, c)
        seat = self.seats[r][c]
        if seat == '.':
            return '.'

        if seat == 'L' and near == 0:
            return '#'
        
        if seat == '#' and near >= 5:
            return 'L'
        
        return seat

    def tick(self):
        # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
        # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
        # Otherwise, the seat's state does not change.
        next_seats = []

        for r in range(self.rows):
            row = []
            next_seats.append(row)
            for c in range(self.cols):
                row.append(self.should_occupy(r, c))
        
        print(self.fmt_before_after(self.seats, next_seats))
        if self.seats == next_seats:
            return StopIteration
        else:
            self.seats = next_seats

class App(Problem):
    lineno = 0
    seats = Seats()

    def add_arguments(self):
        """add any args here"""

    def __post_init__(self) -> None:
        """cleanup here"""

    def transformer(self, line: str) -> Optional[Seats]:
        self.lineno += 1

        if not line:
            return None
        self.seats.append(line.strip())

    def run(self):
        self.load_input()
        i = 0

        for i in count(0):
            i += 1
            print('----', i, '----')
            ret = self.seats.tick()
            print(i, self.seats.count_occupied())
            if ret == StopIteration:
                break
