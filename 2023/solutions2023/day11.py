from typing import *
from solutions2023.lib import *

Line = str
Input = List[Line]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg(r'[.#]+')
  input = p.repsep(line, '\n')

class Day11(Advent[Input]):
    year = 2023
    day = 11

    samples = [
'''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      def expand_rows(map: Input):
        expanded = []
        for row in map:
          expanded += [row]
          if all(c == '.' for c in row):
            expanded += [row]
        return expanded

      def transpose(map: Input):
        return list(zip(*map))

      expanded = transpose(expand_rows(transpose(expand_rows(input))))

      galaxies = [
        coord
        for coord in twod.Coord.all_coords(xmax=len(expanded), ymax=max(len(row) for row in expanded))
        if coord.get(expanded) == '#'
      ]

      return sum(
        (g1 - g2).manhatten_distance
        for g1, g2 in itertools.combinations(galaxies, 2)
      )

    def solve2(self, input: Input) -> Any:
      empty_rows = {
        i for i in range(len(input))
        if all(c == '.' for c in input[i])
      }
      transpose = list(zip(*input))
      empty_cols = {
        j for j in range(len(transpose))
        if all(c == '.' for c in transpose[j])
      }

      galaxies = [
        coord
        for coord in twod.Coord.all_coords(xmax=len(input), ymax=len(transpose))
        if coord.get(input) == '#'
      ]

      def distance(g1: twod.Coord, g2: twod.Coord, growth_factor=10) -> int:
        base = (g1 - g2).manhatten_distance
        row_expansion = sum(growth_factor-1 if i in empty_rows else 0 for i in range(min(g1.x, g2.x), max(g1.x, g2.x)))
        col_expansion = sum(growth_factor-1 if j in empty_cols else 0 for j in range(min(g1.y, g2.y), max(g1.y, g2.y)))
        #print(f'{g1} -> {g2} base: {base} row {row_expansion} col {col_expansion}')
        return base + row_expansion + col_expansion

      return sum(distance(g1,g2, growth_factor=1000000) for g1, g2 in itertools.combinations(galaxies, 2))


if __name__ == '__main__':
    Day11().main()
