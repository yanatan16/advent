from typing import *
from advent.lib import *

Patterns = List[str]
Designs = List[str]
Input = Tuple[Patterns, Designs]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  pattern = p.reg(r'[wubrg]+')
  patterns = p.repsep(pattern, ',')
  designs = p.repsep(pattern, '\n')
  input = patterns & (p.lit('\n\n') >> designs)

class Day19(Advent[Input]):
    year = 2024
    day = 19

    samples = [
'''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      patterns, designs = input
      def possible(design: str) -> bool:
        for pattern in patterns:
          if pattern == design:
            return True
          elif pattern == ''.join(design[:len(pattern)]):
            if possible(design[len(pattern):]):
              return True
        return False

      self._print('\n'.join([
        design + ': ' + ('possible' if possible(design) else 'impossible')
        for design in designs
      ]))
      return sum(1 if possible(design) else 0 for design in designs)

    def solve2(self, input: Input) -> Any:
      patterns, designs = input

      @functools.cache
      def n_possible(design: str) -> int:
        if len(design) == 0:
          return 1

        return sum(
          n_possible(design[len(pattern):]) if pattern == ''.join(design[:len(pattern)]) else 0
          for pattern in patterns
        )

      return sum(n_possible(design) for design in tqdm(designs))


if __name__ == '__main__':
    Day19().main()
