from typing import *
from advent.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#]+')
  n = UtilityParsers.integer
  line = n
  input = p.repsep(line, '\n')

class Day6(Advent[Input]):
    year = 2024
    day = 6

    samples = [

    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
        return 'Not implemented'

    def solve2(self, input: Input) -> Any:
        return 'Not implemented'

if __name__ == '__main__':
    Day6().main()
