from typing import *
from advent.lib import *

Input = List[List[int]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.rep(UtilityParsers.digit)
  input = p.repsep(line, '\n')

class Day10(Advent[Input]):
    year = 2024
    day = 10

    samples = [
'''0123
1234
8765
9876''',
      '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      trailheads = [
        coord
        for coord in twod.Coord.all_coords(input)
        if coord.get(input) == 0
      ]

      def uphill(step: twod.Coord) -> List[twod.Coord]:
        height: int = step.get(input, wrapped=True)
        accessible = [
          node for node in step.neighbors()
          if node.get(input, wrapped=True) == height + 1
          and node.inbounds(input)
        ]
        return accessible

      walkable = {
        trailhead: walk_bfs(
            trailhead,
            uphill,
        )
        for trailhead in trailheads
      }

      scores = {
        trailhead: sum(
          1 if node.get(input, wrapped=True) == 9 else 0
          for node in destset
        )
        for trailhead, destset in walkable.items()
      }

      self._print('scores', scores)

      return sum(scores.values())

    def solve2(self, input: Input) -> Any:
      trailheads = [
        coord
        for coord in twod.Coord.all_coords(input)
        if coord.get(input) == 0
      ]

      def uphill(step: twod.Coord) -> List[twod.Coord]:
        height: int = step.get(input, wrapped=True)
        accessible = [
          node for node in step.neighbors()
          if node.get(input, wrapped=True) == height + 1
          and node.inbounds(input)
        ]
        return accessible

      paths = {
        trailhead: walk_dfs(
          trailhead,
          uphill,
          lambda node: node.get(input, wrapped=True) == 9
        )
        for trailhead in trailheads
      }

      scores = {
        trailhead: len(pathlist)
        for trailhead, pathlist in paths.items()
      }

      self._print('scores', scores)

      return sum(scores.values())

if __name__ == '__main__':
    Day10().main()
