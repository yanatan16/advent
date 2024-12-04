from typing import *
from advent.lib import *
import re

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.rep(p.reg('.'))
  input = p.repsep(line, '\n')



  


class Day4(Advent[Input]):
    year = 2024
    day = 4

    samples = [
      '''..X...
.SAMX.
.A..A.
XMAS.S
.X....''',
'''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX''',
      '''
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      def upright_diagnols(input: Input):
        for i in range(len(input) * 2):
          diag = []
          for j in range(len(input[0])):
            if 0 <= i - j <= len(input) - 1:
              diag += [input[i-j][j]]

          if len(diag) > 3:
            yield diag


      def downleft_diagnols(input: Input):
        for i in range(-len(input), len(input)):
          diag = []
          for j in range(len(input[0])):
            if 0 <= i + j <= len(input) - 1:
              diag += [input[i+j][j]]

          if len(diag) > 3:
            yield diag

      rows = input
      cols = list(zip(*input))
      upright = list(upright_diagnols(input))
      downleft = list(downleft_diagnols(input))

      all_lines = rows + cols + upright + downleft

      def count_occ(line: List[str] | str, item: str):
        if not isinstance(line, str):
          line = ''.join(line)

        result = len(re.findall(item, line))
        self._print(f"count_occ({line}, {item}) = {result}")
        return result

      return sum(
        count_occ(line, 'XMAS') + count_occ(reversed(line), 'XMAS')
        for line in all_lines
      )

    def solve2(self, input: Input) -> Any:
      def square_matches(i:int, j:int):
        diags = [''.join([input[i-1][j-1], input[i][j], input[i+1][j+1]]),
                 ''.join([input[i+1][j-1], input[i][j], input[i-1][j+1]])]
        return all(diag in ('MAS', 'SAM') for diag in diags)

      a_positions = [
        (i,j)
        for i in range(len(input))
        for j in range(len(input[0]))
        if input[i][j] == 'A'
      ]

      a_positions_off_edges = [
        (i,j)
        for i,j in a_positions
        if i > 0 and i < len(input) - 1
        and j > 0 and j < len(input[0]) - 1
      ]

      return sum(
        1 if square_matches(i,j) else 0
        for i,j in a_positions_off_edges
      )



if __name__ == '__main__':
    Day4().main()
