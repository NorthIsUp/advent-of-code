from abc import abstractmethod
from pathlib import Path
import inspect
from typing import Generator, Generic, Iterable, List, TypeVar, cast
from argparse import ArgumentParser, Namespace

T = TypeVar("T")

from logging import getLogger


class Problem(Generic[T]):
    newline_delimiter: str = '\n'

    def __init__(self) -> None:
        self.argument_parser = ArgumentParser()
        self.add_argument = self.argument_parser.add_argument
        self.add_argument('--input', default='input.txt')
        self.add_argument('--example', nargs='?', dest='input', const='input.example.txt')
        self.add_arguments()
        self.args, self.unknown_args = self.argument_parser.parse_known_args()

        self.__post_init__()

    def __post_init__(self) -> None:
        """pass"""

    def __iter__(self) -> Generator[T, None, None]:
        with open(self.root / self.args.input) as input_file:
            for line in self.split_input(input_file.read()):
                yield self.transformer(line)

    def split_input(self, input: str) -> Iterable[str]:
        return input.split(self.newline_delimiter)

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
    def transformer(self, line: str) -> T:
        """transform a line into whatever"""
        return cast(T, line)

    @abstractmethod
    def run(self):
        """runs the thing"""

    def add_arguments(self) -> None:
        """add arguments to self.argument_parser"""

    def main(self) -> int:
        return self.run()
