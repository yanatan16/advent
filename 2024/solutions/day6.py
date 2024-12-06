from typing import *
from advent.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#^]+')
  input = p.repsep(mapline, '\n')

class Day6(Advent[Input]):
    year = 2024
    day = 6

    samples = [
'''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def sim(self, input: Input, guard_pos: twod.Coord, facing: str) -> (bool, Set[Tuple[twod.Coord, str]]):
      visited_vectors = set()

      rotations = {'up': 'right', 'right': 'down', 'down': 'left', 'left': 'up'}

      while (guard_pos, facing) not in visited_vectors and guard_pos.inbounds(input):
        visited_vectors.add((guard_pos, facing))

        next_pos = guard_pos.move(facing)
        if next_pos.get(input) == '#':
          facing = rotations[facing]
        else:
          guard_pos = next_pos

      in_loop = guard_pos.inbounds(input)
      return in_loop, visited_vectors

    def solve1(self, input: Input) -> Any:
      guard_pos = [coord for coord in twod.Coord.all_coords(input) if coord.get(input) in '^'][0]

      _, visited_vectors = self.sim(input, guard_pos, 'up')

      return len({pos for pos, _ in visited_vectors})

    def add_obstruction(self, input: Input, obs: twod.Coord) -> Input:
      new_input = [[v for v in row] for row in input]
      obs.set(new_input, '#')
      return new_input

    def solve2(self, input: Input) -> Any:
      guard_pos = [coord for coord in twod.Coord.all_coords(input) if coord.get(input) in '^'][0]
      _, visited_vectors = self.sim(input, guard_pos, 'up')
      positions = {pos for pos, _ in visited_vectors if pos != guard_pos}

      total = 0

      for position in tqdm(positions):
        in_loop, _ = self.sim(self.add_obstruction(input, position), guard_pos, 'up')
        if in_loop:
          total += 1
          self._print(f'Found in loop for obstruction at {position}')

      return total



if __name__ == '__main__':
    Day6().main()
