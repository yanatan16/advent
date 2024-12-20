from typing import *
from advent.lib import *
from advent.lib.twod import *
from advent.lib.binary_search import *

Input = List[Coord]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = UtilityParsers.integer
  coord = p.repsep(n, ',', min=2, max=2) > (lambda p: Coord(*p))
  input = p.repsep(coord, '\n')

class Day18(Advent[Input]):
    year = 2024
    day = 18

    samples = [
'''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      xmax = ymax = 71 if len(input) >= 500 else 7
      sim = 1024 if len(input) >= 500 else 12
      corrupted = {c for c in input[:sim]}
      start = Coord(0,0)
      end = Coord(xmax-1,ymax-1)

      nodes = set(Coord.all_coords(xmax, ymax)) - corrupted

      self._print(printnodes({
        '.': nodes - {start},
        '#': corrupted,
        '@': [start]
      }, xmax, ymax))

      distances, self._previous = djikstras(
        nodes = nodes,
        start = start,
        neighbor = lambda node: [
          (nn, 1)
          for nn in node.neighbors()
          if nn.inbounds(xmax, ymax)
          and nn not in corrupted
        ]
      )

      return distances[end]

    def solve2(self, input: Input) -> Any:
      xmax = ymax = 71 if len(input) >= 500 else 7
      sim = 1024 if len(input) >= 500 else 12
      corrupted = {c for c in input[:sim]}
      start = Coord(0,0)
      end = Coord(xmax-1,ymax-1)
      all_nodes = set(Coord.all_coords(xmax, ymax))

      @functools.cache
      def not_passable(x: int) -> bool:
        corrupted = {c for c in input[:x]}
        dist, _ = djikstras(
          nodes = all_nodes - corrupted,
          start = start,
          neighbor = lambda node: [
            (nn, 1)
            for nn in node.neighbors()
            if nn.inbounds(xmax, ymax)
            and nn not in corrupted
          ],
          _tqdm=False
        )
        return dist[end] == float('inf')

      return input[binary_search_bool(sim, len(input), not_passable) - 1]

if __name__ == '__main__':
    Day18().main()
