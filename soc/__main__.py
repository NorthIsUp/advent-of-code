import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("day", type=int)
args, unknown = parser.parse_known_args()

mod = __import__(f"soc.day{args.day}", fromlist=["App"])
ret_code = mod.App().main()
sys.exit(ret_code)
