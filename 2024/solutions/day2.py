from typing import *
from advent.lib import *

Input = List[List[int]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#]+')
  n = UtilityParsers.integer
  line = p.rep(n)
  input = p.repsep(line, '\n')

class Day2(Advent[Input]):
    year = 2024
    day = 2

    samples = [
'''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    @staticmethod
    def is_safe(report: List[int]) -> bool:
        diffs = [x - y for x, y in zip(report, report[1:])]
        # Direction of differences (-1 or 1)
        dirs = [diff / abs(diff) if diff != 0 else 0 for diff in diffs]
        # Magnitude of differences (absolute values)
        mags = [abs(diff) for diff in diffs]

        return all(dir == dirs[0] for dir in dirs) and all(0 < mag < 4 for mag in mags)

    def solve1(self, input: Input) -> Any:
      return sum(1 if self.is_safe(report) else 0 for report in input)

    def is_safe_removing_a_level(self, report: List[int]) -> bool:
      # Naive method should work for day 2
      if self.is_safe(report):
        return True

      for i in range(len(report)):
        if self.is_safe(report[:i] + report[(i+1):]):
          return True
      else:
        return False

    def solve2(self, input: Input) -> Any:
      return sum(1 if self.is_safe_removing_a_level(report) else 0 for report in input)

if __name__ == '__main__':
    Day2().main()
