from typing import *
from solutions2023.lib import *

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg(r'[.#S]+')
  input = p.repsep(line, '\n')

class Day21(Advent[Input]):
    year = 2023
    day = 21

    samples = [
'''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def walk(self, input: Input, n:int) -> int:
      start = [c for c in twod.Coord.all_coords(input) if c.get(input) == 'S'][0]

      q = {start}
      for step in range(n):
        q = {
          neighbor
          for coord in q
          for neighbor in coord.neighbors()
          if neighbor.wrap(input).get(input) in '.S'
        }

      debug(f'walk({n}) = {len(q)}')
      return len(q)

    def solve1(self, input: Input, s=None, n= None) -> Any:
      return self.walk(input, 64 if len(input) > 30 else 6)

    def solve2(self, input: Input) -> Any:
      w = h = len(input)

      target = 26501365 if len(input) > 30 else 5000

      rem = target % w

      polypoints = [rem, rem+w, rem+2*w]
      polyvals = [self.walk(input, p) for p in polypoints]

      coeffs = np.polyfit([0,1,2], polyvals, deg=2)
      return np.polyval(coeffs, target // w).round().astype(int)


if __name__ == '__main__':
    Day21().main()
