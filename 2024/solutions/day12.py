from typing import *
from advent.lib import *

Input = List[List[str]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  char = p.reg(r'[A-Za-z0-9]')
  mapline = p.rep(char)
  input = p.repsep(mapline, '\n')

class Day12(Advent[Input]):
    year = 2024
    day = 12

    samples = [
'''AAAA
BBCD
BBCC
EEEC''',
      '''OOOOO
OXOXO
OOOOO
OXOXO
OOOOO''',
      '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE''',
      '''EEEEE
EXXXX
EEEEE
EXXXX
EEEEE'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def find_regions(self, input: Input) -> Generator[Set[twod.Coord], None, None]:
      unfound = set(twod.Coord.all_coords(input))

      def connected(node: twod.Coord) -> List[twod.Coord]:
        return [
          n for n in node.neighbors()
          if n.inbounds(input)
          and n.get(input) == node.get(input)
        ]

      while len(unfound) > 0:
        region = walk_bfs(unfound.pop(), connected)
        unfound = unfound.difference(region)
        yield region

    def area(self, region: Set[twod.Coord]) -> int:
      return len(region)

    def perimeter(self, region: Set[twod.Coord], input: Input) -> int:
      return sum(
        1 if n not in region else 0
        for node in region
        for n in node.neighbors()
      )

    def solve1(self, input: Input) -> Any:
      if self._verbose:
        for region in self.find_regions(input):
          self._print(f'region {list(region)[0].get(input)} {region} {self.area(region)} {self.perimeter(region, input)}')

      return sum(
        self.area(region) * self.perimeter(region, input)
        for region in self.find_regions(input)
      )


    def sides(self, region: Set[twod.Coord], input: Input) -> int:
      def _sides(dir: twod.Direction) -> int:
        count = 0
        rset = {c for c in region}
        while len(rset) > 0:
          node = rset.pop()
          if node.get(input) == node.move(dir).get(input):
            continue
          else:
            count += 1
            val = node.get(input)
            left = twod.left_turn[dir]
            right = twod.right_turn[dir]

            # Go left and right and remove nodes on this side
            nn = node
            while nn.move(left).get(input) == val and nn.move(left).move(dir).get(input) != val:
              nn = nn.move(left)
              if nn in rset:
                rset.remove(nn)

            nn = node
            while nn.move(right).get(input) == val and nn.move(right).move(dir).get(input) != val:
              nn = nn.move(right)
              if nn in rset:
                rset.remove(nn)

        return count

      return sum(_sides(dir) for dir in twod.directions)

    def solve2(self, input: Input) -> Any:
      return sum(
        self.area(region) * self.sides(region, input)
        for region in self.find_regions(input)
      )

if __name__ == '__main__':
    Day12().main()
