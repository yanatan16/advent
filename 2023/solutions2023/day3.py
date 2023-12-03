from typing import *
from solutions2023.lib import *

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg('.*')
  input = p.repsep(line, '\n')

numbers = '0123456789'
symbols = '!@#$%^&*()<>?/,;:{}[]-=_+~'
period = '.'

class Day3(Advent[Input]):
    year = 2023
    day = 3

    samples = [
'''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      debug = False

      gearmap = collections.defaultdict(lambda: [])

      total = 0
      for rowi in range(len(input)):
        row = input[rowi]
        colj = 0
        while colj < len(row):
          if row[colj] in numbers:
            partlen = 1
            while colj+partlen < len(row) and row[colj+partlen] in numbers:
              partlen += 1
            colend = colj+partlen
            partstr = ''.join(row[colj:colend])

            adj = [
              (input[i][j], (i,j))
              for i in range(rowi-1, rowi+2)
              for j in range(colj-1, colend+1)
              if 0 <= i < len(input)
              and 0 <= j < len(row)
            ]

            if any(c in symbols for c, _ in adj):
              if debug:
                print(f'Part {partstr} is adjacent to a part: {adj}')
              total += int(partstr)
            else:
              if debug:
                print(f'Part {partstr} is NOT adjacent to a part')

            for c, pos in adj:
              if c == '*':
                gearmap[pos] += [int(partstr)]

            colj += partlen
          else:
            colj += 1

      part2 = 0
      for gearpos, gearadj in gearmap.items():
        if len(gearadj) == 2:
          part2 += gearadj[0]*gearadj[1]

      return total, part2

    def solve2(self, input: Input) -> Any:
      return 'See part 1'

if __name__ == '__main__':
    Day3().main()
