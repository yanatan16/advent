from typing import *
from dataclasses import dataclass
import itertools, collections, functools
from enum import Enum
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

Input = List[List[bool]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  infected = p.lit('#') >> p.success(True)
  clean = p.lit('.') >> p.success(False)
  row = p.rep(infected | clean)
  input = p.repsep(row, '\n')

class State(Enum):
  clean = '.'
  weakened = 'W'
  infected = '#'
  flagged = 'F'

class Day22(Advent[Input]):
    day = 22

    samples = [
'''..#
#..
...'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      debug = len(input) == 3
      grid = SparseGrid(default_value=False)

      assert len(input) % 2 == 1
      assert len(input[0]) % 2 == 1
      assert len(input) == len(input[0])
      halfcenterlength = int(len(input) / 2)
      center = twod.Coord(halfcenterlength, halfcenterlength)

      for i in range(len(input)):
        for j in range(len(input[0])):
          if input[i][j]:
            grid.set(twod.Coord(i-halfcenterlength, j-halfcenterlength),
                     True)

      cur = twod.Coord(0,0)
      dir:twod.Direction = 'up'
      infections = 0

      for step in range(10000):
        if debug and step < 7:
          print(f'step {step+1}: {infections} {cur} {dir}')
          print(grid.twodstr(lambda infected: '#' if infected else '.'))

        infected = grid[cur]
        dir = twod.right_turn[dir] if infected else twod.left_turn[dir]
        grid.set(cur, not infected)
        if not infected:
          infections += 1
        cur = cur.move(dir)

      return infections

    def solve2(self, input: Input) -> Any:
      grid = SparseGrid(default_value=State.clean)

      halfcenterlength = int(len(input) / 2)
      center = twod.Coord(halfcenterlength, halfcenterlength)

      for i in range(len(input)):
        for j in range(len(input[0])):
          if input[i][j]:
            grid.set(twod.Coord(i-halfcenterlength, j-halfcenterlength),
                     State.infected)

      cur = twod.Coord(0,0)
      dir:twod.Direction = 'up'
      infections = 0

      for step in tqdm(range(10000000)):

        if len(input) == 3 and step < 7:
          print(f'step {step+1}: {infections} {cur} {dir}')
          print(grid.twodstr(lambda state: state.value))

        match grid[cur]:
          case State.clean:
            dir = twod.left_turn[dir]
            grid.set(cur, State.weakened)
          case State.weakened:
            infections += 1
            grid.set(cur, State.infected)
          case State.infected:
            dir = twod.right_turn[dir]
            grid.set(cur, State.flagged)
          case State.flagged:
            dir = twod.right_turn[twod.right_turn[dir]]
            grid.clear(cur)

        cur = cur.move(dir)

      return infections

if __name__ == '__main__':
    Day22().main()
