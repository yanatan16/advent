from typing import *
from solutions2023.lib import *

from .day9 import diff, repdiff

Map = List[str]
Input = Map

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg('[.#O]+')
  input = p.repsep(line, '\n')

class Day14(Advent[Input]):
    year = 2023
    day = 14

    samples = [
'''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def move_boulder_north(self, map: Map, i: int, j: int):
      assert map[i][j] == 'O'
      map[i][j] = '.'

      for upi in range(i-1, -1, -1):
        if map[upi][j] in 'O#':
          map[upi+1][j] = 'O'
          return

      map[0][j] = 'O'

    def move_boulder_west(self, map: Map, i: int, j: int):
      assert map[i][j] == 'O'
      map[i][j] = '.'

      for jj in range(j-1, -1, -1):
        if map[i][jj] in 'O#':
          map[i][jj+1] = 'O'
          return

      map[i][0] = 'O'

    def move_boulder_south(self, map: Map, i: int, j: int):
      assert map[i][j] == 'O'
      map[i][j] = '.'

      for ii in range(i+1, len(map)):
        if map[ii][j] in 'O#':
          map[ii-1][j] = 'O'
          return

      map[len(map)-1][j] = 'O'

    def move_boulder_east(self, map: Map, i: int, j: int):
      assert map[i][j] == 'O'
      map[i][j] = '.'

      for jj in range(j+1, len(map[0])):
        if map[i][jj] in 'O#':
          map[i][jj-1] = 'O'
          return

      map[i][len(map[0])-1] = 'O'

    def tilt_north(self, map: Map):
      for i in range(len(map)):
        for j in range(len(map[0])):
          if map[i][j] == 'O':
            self.move_boulder_north(map, i, j)

    def tilt_south(self, map: Map):
      for i in range(len(map)-1, -1, -1):
        for j in range(len(map[0])):
          if map[i][j] == 'O':
            self.move_boulder_south(map, i, j)

    def tilt_west(self, map: Map):
      for j in range(len(map[0])):
        for i in range(len(map)):
          if map[i][j] == 'O':
            self.move_boulder_west(map, i, j)

    def tilt_east(self, map: Map):
      for j in range(len(map[0])-1, -1, -1):
        for i in range(len(map)):
          if map[i][j] == 'O':
            self.move_boulder_east(map, i, j)

    def transpose(self, map: Map) -> Map:
      return [list(row) for row in zip(*map)]

    def tilt_cycle(self, map: Map) -> Map:
      self.tilt_north(map)
      self.tilt_west(map)
      self.tilt_south(map)
      self.tilt_east(map)

    def load(self, map: Map):
      return sum(
        len(map) - c.x
        for c in twod.Coord.all_coords(map)
        if c.get(map) == 'O'
      )

    def print(self, map: Map):
      debug('=====')
      debug('\n'.join(''.join(row) for row in map))


    def solve1(self, input: Input) -> Any:
      map = [[c for c in row] for row in input]
      self.tilt_north(map)
      return self.load(map)


    def solve2(self, input: Input) -> Any:
      map = [[c for c in row] for row in input]
      loads = collections.defaultdict(lambda: [])
      target = 1000000000

      for i in tqdm(range(10000)):
        self.tilt_cycle(map)
        load = self.load(map)
        loads[load] += [i+1]

      for load, steps in loads.items():
        if len(steps) < 20:
          continue
        rd = repdiff(steps[-100:])
        if len(rd) == 3:
          base = steps[-1]
          inc = rd[1][0]
          int((target - base) / inc)
          print(f'Load {load} has a constant growth of {rd[1][0]} from {steps[-1]}')

          if (target - base) % inc == 0:
            return load




if __name__ == '__main__':
    Day14().main()
