import sys
from pathlib import Path

template = '''from typing import *
from dataclasses import dataclass
fro enum import Enum
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \\t]*'):
  input = p.repsep(UtilityParsers.integer, ',')

class DayXX(Advent[Input]):
    day = XX

    samples = [

    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
        return 'Not implemented'

    def solve2(self, input: Input) -> Any:
        return 'Not implemented'

if __name__ == '__main__':
    DayXX().main()
'''

def main():
    assert len(sys.argv) > 1
    assert isinstance(int(sys.argv[1]), int)

    day = sys.argv[1]
    output = template.replace('XX', day)
    fp = Path(__file__).parent / f'day{day}.py'

    if fp.exists():
        raise RuntimeError(f'I wont overwrite {fp}')

    with fp.open('w') as f:
        f.write(output)

    print(f'{fp} written and ready!')

if __name__ == '__main__':
    main()
