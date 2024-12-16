from typing import *
from advent.lib import *

Input = List[List[str]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#SE]+') > (lambda line: [l for l in line])
  input = p.repsep(mapline, '\n')

class Day16(Advent[Input]):
    year = 2024
    day = 16

    samples = [
'''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############''',
      '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      start = [c for c in twod.Coord.all_coords(input) if c.get(input) == 'S'][0]
      end = [c for c in twod.Coord.all_coords(input) if c.get(input) == 'E'][0]
      positions = {c for c in twod.Coord.all_coords(input) if c.get(input) in 'SE.'}

      Node = Tuple[twod.Coord, twod.Direction]
      start_node = (start, 'right')
      nodes = [(pos, dir) for pos in positions for dir in twod.directions]

      def neighbor(node: Node) -> Generator[Tuple[Node, float], None, None]:
        pos, dir = node
        if pos.move(dir) in positions:
          yield ((pos.move(dir), dir), 1)
        yield ((pos, twod.left_turn[dir]), 1000)
        yield ((pos, twod.right_turn[dir]), 1000)

      distances, previous = djikstras(
        nodes, start_node, neighbor
      )
      self._distances = distances
      self._previous = previous

      return min(
        score
        for node, score in distances.items()
        if node[0] == end
      )

    def solve2(self, input: Input) -> Any:
      start = [c for c in twod.Coord.all_coords(input) if c.get(input) == 'S'][0]
      end = [c for c in twod.Coord.all_coords(input) if c.get(input) == 'E'][0]
      positions = {c for c in twod.Coord.all_coords(input) if c.get(input) in 'SE.'}

      assert self._previous
      assert self._distances

      minscore = min(
        score
        for node, score in self._distances.items()
        if node[0] == end
      )

      unvisited = {node for node, score in self._distances.items()
                   if node[0] == end and score == minscore}
      found = set()

      while len(unvisited):
        node = unvisited.pop()
        found.add(node)

        for pn in self._previous[node]:
          if pn not in found:
            unvisited.add(pn)

      return len({pos for pos, _ in found})


if __name__ == '__main__':
    Day16().main()
