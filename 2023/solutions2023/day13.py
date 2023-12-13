from typing import *
from solutions2023.lib import *

Pattern = List[List[str]]
Input = List[Pattern]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  pattern = p.repsep(p.reg(r'[.#]+'), '\n')
  input = p.repsep(pattern, '\n\n')

def find_reflection(pattern: Pattern) -> int:
  for i in range(1, len(pattern)):
    if i > len(pattern) - i:
      if pattern[i:] == pattern[(2*i - len(pattern)):i][::-1]:
        return i
    else:
      if pattern[:i] == pattern[i:(2*i)][::-1]:
        return i

  return 0

def difference_count(p1: Pattern, p2: Pattern) -> int:
  return sum(
    1 if c1 != c2 else 0
    for r1, r2 in zip(p1, p2)
    for c1, c2 in zip(r1, r2)
  )


def find_smudged_reflection(pattern: Pattern) -> int:
  for i in range(1, len(pattern)):
    if i > len(pattern) - i:
      if difference_count(pattern[i:], pattern[(2*i - len(pattern)):i][::-1]) == 1:
        return i
    else:
      if difference_count(pattern[:i], pattern[i:(2*i)][::-1]) == 1:
        return i

  return 0

def transpose(pattern: Pattern):
  return list(zip(*pattern))

class Day13(Advent[Input]):
    year = 2023
    day = 13

    samples = [
'''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      for pattern in input:
        if find_reflection(pattern) * 100 + find_reflection(transpose(pattern)) == 0:
          print('Found bad pattern:')
          print('\n'.join(pattern))

      return sum(
        find_reflection(pattern) * 100 + find_reflection(transpose(pattern))
        for pattern in input
      )

    def solve2(self, input: Input) -> Any:
      for pattern in input:
        if find_smudged_reflection(pattern) * 100 + find_smudged_reflection(transpose(pattern)) == 0:
          print('Found bad pattern:')
          print('\n'.join(pattern))

      return sum(
        find_smudged_reflection(pattern) * 100 + find_smudged_reflection(transpose(pattern))
        for pattern in input
      )



if __name__ == '__main__':
    Day13().main()
