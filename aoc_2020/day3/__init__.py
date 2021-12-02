from typing import Generator, Iterable, List, Tuple, Union
from soc.problem import Problem
from itertools import count
from functools import reduce

class TobogganHill:
    def __init__(self, treemap: List[str]) -> None:
        self.width: int = len(treemap[0])
        self.height: int = len(treemap)
        self.treemap: List[str] = treemap

    def __getitem__(self, xy: Union[int, Tuple[int, int]]):
        x, y = [xy, None] if isinstance(xy, int) else xy
        assert isinstance(x, int)

        assert x < len(self.treemap), f"ran out of hill {x} > {self.height}"
        return self.treemap[x] if y is None else self.treemap[x][y % self.width]


class App(Problem):
    def __init__(self) -> None:
        super().__init__()
        self.hill = TobogganHill(self.lines)

    def add_arguments(self) -> None:
        self.add_argument("--slopes", default="1/3,")
        self.add_argument("--starts", type=int, default=0)

    def run(self):
        solution = 1
        for over, down in self.slopes:
            # assert self.hill.height % down == 0, f"{self.hill.height} % {down} == {self.hill.height % down}"
            for i in self.starting_positions:
                run_solution = self.toboggan_run(i, down, over)
                print(f'>> we hit {run_solution} trees')
                solution *= run_solution


        print(solution)

    def toboggan_run(self, i: int, down: int, over: int) -> int:
        print("-" * 80)
        print("over", over, "down", down)
        hill = self.hill
        trees = 0
        i, j = 0, 0
        for i in range(0, hill.height):
            if i % down == 0:
                trees += self.path(i, j)
                j += over
            else:
                print(f"{i:03} - {hill[i]}")
        return trees


    def path(self, i: int, j: int) -> int:
        hill = self.hill
        is_tree = self.hill[i, (j % hill.width)] == "#"
        line = "".join(
            ("X" if is_tree else "O")
            if (j % hill.width) == (x % hill.width)
            else hill[i, x]
            for x in range(0, hill.width)
        )
        print(f"{i:03} > {line}")
        return int(is_tree)

    @property
    def slopes(self) -> Generator[Tuple[int, int], None, None]:
        for slope in self.args.slopes.split(","):
            over, down = slope.split("/")
            yield int(over), int(down)

    @property
    def starting_positions(self) -> Generator[int, None, None]:
        yield from (
            [self.args.starts] if self.args.starts >= 0 else range(self.hill.width)
        )


# 177 too low
# 456 too low
# 3313416600 too low
