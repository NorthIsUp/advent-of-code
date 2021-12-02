import sys
from argparse import ArgumentParser
from inspect import cleandoc
from pathlib import Path
from subprocess import run

from .template import problem_template

parser = ArgumentParser()
parser.add_argument("day", type=int)
parser.add_argument("--start", action='store_true')
args, unknown = parser.parse_known_args()

if args.start:
    root = Path(__file__).parent
    day_path = root / f'day{args.day}'
    day_path.mkdir(exist_ok=True)
    day_init = day_path / '__init__.py'
    day_input = day_path / 'input.txt'

    if not day_init.exists():
        day_init.write_text(problem_template)

    if not day_input.exists():
        run(
            [
                'curl',
                f'https://adventofcode.com/2021/day/{args.day}/input',
                '-H', 'Cookie: session=53616c7465645f5f06fd93f57465e98f030c5742f3499920d4dc48df67398e74de34f7ef7c0a7a50c5696b6941a4eaf4',
                '-o', 'input.txt'
            ],
            cwd=day_path
        )

    sys.exit(0)

mod = __import__(f"soc.day{args.day}", fromlist=["App"])
ret_code = mod.App().main()
sys.exit(ret_code)
