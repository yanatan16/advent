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

    def solve1(self, input: Input) -> Any:
      all_coords = twod.Coord.all_coords(input)
      start = [c for c in all_coords if c.get(input) == 'S'][0]

      q = {start}
      for step in range(64 if len(input) > 30 else 6):
        # debug(f'Step {step+1}')
        # debug('\n'.join(
        #   ''.join(
        #     'O' if twod.Coord(i,j) in q
        #     else twod.Coord(i,j).get(input)
        #     for j in range(len(input[0]))
        #   )
        #   for i in range(len(input))
        # ))

        q = {
          neighbor
          for coord in q
          for neighbor in coord.neighbors()
          if neighbor.get(input) in '.S'
        }

      return len(q)

    def solve2(self, input: Input) -> Any:
      all_coords = twod.Coord.all_coords(input)
      start = [c for c in all_coords if c.get(input) == 'S'][0]

      q = {start}
      for step in tqdm(range(26501365 if len(input) > 30 else 100)):
        if step in (6, 10, 50, 100, 500, 1000, 5000):
          debug(f'Step {step}: {len(q)}')

        q = {
          neighbor.wrap(input)
          for coord in q
          for neighbor in coord.neighbors()
          if neighbor.wrap(input).get(input) in '.S'
        }

      return len(q)

if __name__ == '__main__':
    Day21().main()
