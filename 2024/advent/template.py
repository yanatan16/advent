import sys
from pathlib import Path

template = '''from typing import *
from advent.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \\t]*'):
  mapline = p.reg(r'[.#]+')
  n = UtilityParsers.integer
  line = n
  input = p.repsep(line, '\\n')

class DayXX(Advent[Input]):
    year = 2024
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
    fp = Path(__file__).parent.parent / "solutions" / f'day{day}.py'

    if fp.exists():
        raise RuntimeError(f'I wont overwrite {fp}')

    with fp.open('w') as f:
        f.write(output)

    print(f'{fp} written and ready!')

if __name__ == '__main__':
    main()
