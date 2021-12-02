import sys
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from subprocess import run

from . import template

parser = ArgumentParser()
parser.add_argument("day", type=int)
parser.add_argument("--start", action='store_true')
parser.add_argument('--session', default='53616c7465645f5f68c18c0c63ff879705d7d1ce7a38a6e1cef37860c6422db1eaf0851394311e2ee1f50eac24e5b352')

args, unknown = parser.parse_known_args()

if args.start:
    root = Path(__file__).parent
    day_path = root / f'day{args.day}'
    day_path.mkdir(exist_ok=True)

    day_init = day_path / '__init__.py'
    day_input = day_path / 'input.txt'
    day_problem = day_path / 'problem.txt'

    if not day_init.exists():
        day_init.write_text(getsource(template))

    if not day_input.exists() or 'before it unlocks!' in day_input.read_text():
        run(
            [
                'curl',
                f'https://adventofcode.com/2021/day/{args.day}/input',
                '-H', f'Cookie: session={args.session}',
                '-o', day_input
            ],
        )

    if not day_problem.exists() or 'before it unlocks!' in day_problem.read_text():
        run(
            [
                'curl',
                f'https://adventofcode.com/2021/day/{args.day}',
                '-H', f'Cookie: session={args.session}',
                '-o', day_problem
            ],
        )

    sys.exit(0)

mod = __import__(f"aoc_2021.day{args.day}", fromlist=["App"])
ret_code = mod.App().main()
sys.exit(ret_code)
