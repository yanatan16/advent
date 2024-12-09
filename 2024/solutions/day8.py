from typing import *
from advent.lib import *

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.0-9a-zA-Z]+')
  input = p.repsep(mapline, '\n')

class Day8(Advent[Input]):
    year = 2024
    day = 8

    samples = [
'''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      antennas = [
        (c, c.get(input))
        for c in twod.Coord.all_coords(input)
        if c.get(input) != '.'
      ]

      freqs = {f for c, f in antennas}

      antinodes = {
        anode
        for freq in freqs
        for c1, c2 in itertools.combinations([c for c, f in antennas if f == freq], 2)
        for anode in (c2 + c2 - c1, c1 + c1 - c2)
        if anode.inbounds(input)
      }

      return len(antinodes)

    def solve2(self, input: Input) -> Any:
      antennas = [
        (c, c.get(input))
        for c in twod.Coord.all_coords(input)
        if c.get(input) != '.'
      ]

      freqs = {f for c, f in antennas}

      def calc_antinodes(c1: twod.Coord, c2: twod.Coord) -> Generator[twod.Coord, None, None]:
        diff = (c2 - c1)
        for p, inc in ((c1, diff), (c2, -diff)):
          while p.inbounds(input):
            yield p
            p = p + inc


      antinodes = {
        anode
        for freq in freqs
        for c1, c2 in itertools.combinations([c for c, f in antennas if f == freq], 2)
        for anode in calc_antinodes(c1, c2)
        if anode.inbounds(input)
      }

      return len(antinodes)

if __name__ == '__main__':
    Day8().main()
