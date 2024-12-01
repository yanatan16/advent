from typing import *
from advent.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#]+')
  n = UtilityParsers.integer
  line = p.rep(n)
  input = p.repsep(line, '\n')

class Day1(Advent[Input]):
    year = 2024
    day = 1

    samples = [
"""3   4
4   3
2   5
1   3
3   9
3   3"""
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      l1, l2 = zip(*input)
      l1 = sorted(l1)
      l2 = sorted(l2)
      return sum(abs(x - y) for x, y in zip(l1, l2))

    def solve2(self, input: Input) -> Any:
      l1, l2 = zip(*input)
      freq = freqs(sorted(l2))
      return sum(
        x * freq.get(x, 0)
        for x in l1
      )

if __name__ == '__main__':
    Day1().main()
