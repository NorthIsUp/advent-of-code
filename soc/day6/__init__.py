from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast
from soc.problem import Problem
from itertools import count
from functools import reduce
from dataclasses import dataclass, field
import re
from pprint import pprint
from collections import Counter


@dataclass
class CustomsForm:
    answers: List[str]
    
    @property
    def unique_answers(self) -> int:
        c = Counter()
        for answer in self.answers:
            c.update(answer)
        print(c)
        return len(c)

    @property
    def union_answers(self) -> int:
        return len(reduce(set.intersection, [set(a) for a in self.answers]))


class App(Problem):
    lineno = 1

    newline_delimiter: str = "\n\n"

    def transformer(self, line: str) -> Optional[CustomsForm]:
        # calculate line no for debug
        lineno = self.lineno
        self.lineno += 2 + sum(_ == '\n' for _ in line)

        if not line.strip():
            return None

        return CustomsForm(answers=line.strip().split('\n'))


    def run(self):
        for c in self:
            print('\n'.join(c.answers))
            print(c.union_answers)
            print()

        print(sum(c.union_answers for c in self))
        # for bp in self:
        #     print(f'{bp.row} {bp.side}: row: {bp.row_number}, col: {bp.column_number}, id: {bp.id}')
