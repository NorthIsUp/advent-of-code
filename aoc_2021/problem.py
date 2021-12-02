from __future__ import annotations

import inspect
from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from functools import singledispatchmethod
from logging import getLogger
from pathlib import Path
from typing import (
    Any,
    Generator,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
    cast,
)

T = TypeVar("T")

@dataclass
class Problem(Generic[T]):
    newline_delimiter: str = '\n'
    loaded_input: List[T] = field(default_factory=list)
    args: Namespace = Namespace()
    unknown_args: Any = None

    def __post_init__(self) -> None:
        parser = ArgumentParser()
    
        parser.add_argument('--input', default='input.txt')
        parser.add_argument('--example', nargs='?', dest='input', const='input.example.txt')
        parser.add_argument('--example2', nargs='?', dest='input', const='input.example2.txt')

        self.add_arguments(parser)

        self.args, self.unknown_args = parser.parse_known_args()

    def __iter__(self) -> Generator[T, None, None]:
        yield from self.loaded_input

    @singledispatchmethod
    def __getitem__(self, i: object) -> object:
        raise NotImplementedError('nope')
    
    @__getitem__.register
    def _(self, i: int) -> T:
        return self.loaded_input[i]

    @__getitem__.register
    def _(self, i: slice) -> Iterable[T]:
        return self.loaded_input[i]

    def __len__(self) -> int:
        return len(self.loaded_input)

    def split_input(self, input: str) -> Iterable[str]:
        return input.split(self.newline_delimiter)

    def load_input(self) -> List[T]:
        assert (self.root / self.args.input).exists(), f'input file "{self.args.input}" missing'
        with open(self.root / self.args.input) as input_file:
            for line in self.split_input(input_file.read()):
                if (to_yield := self.transformer(line)) is not None:
                    self.loaded_input.append(to_yield)
        return self.loaded_input

    def input_chunks(self, size: int = 1, start: int = 0) -> Generator[List[T], None, None]:
        return self.input_windows(size, start, size)

    def input_windows(self, size: int = 1, start: int=0, step: int = 1) -> Generator[List[T], None, None]:
        return (cast(List[T], self[i:i+size]) for i in range(start, len(self), step))

    @property
    def root(self) -> Path:
        return Path(inspect.getfile(self.__class__)).parent

    @property
    def lines(self) -> List[str]:
        """chomp'd list of lines"""
        return [_[:-1] for _ in self]

    @classmethod
    def log(cls, *args, **kwargs) -> None:
        getLogger(cls.__name__).debug(*args, **kwargs)

    @abstractmethod
    def transformer(self, line: str) -> Optional[T]:
        """transform a line into whatever"""
        return cast(T, line)

    @abstractmethod
    def run(self) -> Optional[int]:
        """runs the thing"""

    def add_arguments(self, parser: ArgumentParser) -> None:
        """add arguments to self.argument_parser"""

    def main(self) -> int:
        return self.run() or 0
