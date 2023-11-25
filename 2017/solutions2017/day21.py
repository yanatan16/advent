from typing import *
from dataclasses import dataclass
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

START = '''.#./..#/###'''
DEBUG = False

Grid = List[List[bool]]

def pattern_to_grid(s: str) -> Grid:
  return [[c == '#' for c in line] for line in s.split('/')]

def flipv(g: Grid) -> Grid:
  return g[::-1]

def fliph(g: Grid) -> Grid:
  return [l[::-1] for l in g]

def rot90(g: Grid) -> Grid:
  if len(g) == 2:
    return [[g[1][0], g[0][0]], [g[1][1], g[0][1]]]
  else: # len(g) == 3
    return [[g[2][0], g[1][0], g[0][0]],
            [g[2][1], g[1][1], g[0][1]],
            [g[2][2], g[1][2], g[0][2]]]

def pgrid(g: Grid, sep='/') -> str:
  return sep.join(''.join('#' if c else '.' for c in row) for row in g)

def variations(g: Grid) -> Generator[Grid, None, None]:
  for h in (g, flipv(g), fliph(g), flipv(fliph(g))):
    yield h
    yield rot90(h)
    yield rot90(rot90(h))
    yield rot90(rot90(rot90(h)))

def split(g: Grid, subsize: int) -> List[List[Grid]]:
  assert len(g) % subsize == 0
  n = int(len(g) / subsize)
  return [[[[g[i*subsize + ii][j*subsize + jj]
             for jj in range(subsize)]
            for ii in range(subsize)]
           for j in range(n)]
          for i in range(n)]

def join(gs: List[List[Grid]]) -> Grid:
  n = len(gs)
  subsize = len(gs[0][0])
  outsize = subsize*n
  return [[gs[int(i/subsize)][int(j/subsize)][i%subsize][j%subsize]
           for j in range(outsize)]
          for i in range(outsize)]

class Rule(NamedTuple):
  input: Grid
  output: Grid

  @property
  def size(self):
    return len(self.input)

  def matches(self, test: Grid) -> bool:
    if len(test) != self.size:
      return False

    for g in variations(test):
      if g == self.input:
        if DEBUG:
          print(f'Rule {pgrid(self.input)} matches {pgrid(test)} with variation {pgrid(g)}')
        return True

def enhance(g: Grid, rules: List[Rule]) -> Grid:
  for rule in rules:
    if rule.matches(g):
      return rule.output

  assert False, f'enhancement failed for {pgrid(g)}'

def counton(g:Grid) -> int:
  return sum(sum(1 if c else 0 for c in row) for row in g)

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  pattern = p.reg(r'[.#/]+') > pattern_to_grid
  sep = p.lit('=>')
  line = ((pattern << sep) & pattern) > (lambda pair: Rule(*pair))
  input = p.repsep(line, '\n')

Input = List[Rule]

class Day21(Advent[Input]):
    day = 21

    samples = [
'''../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#''',
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      grid = pattern_to_grid(START)

      for step in range(5 if len(input) > 2 else 2):
        if DEBUG:
          print(f'Step {step}: ({counton(grid)}): Grid')
          print(pgrid(grid, sep="\n"))

        if len(grid) % 2 == 0:
          subgrids = split(grid, 2)
        else:
          subgrids = split(grid, 3)

        enhanced_subgrids = [[enhance(g, rules=input) for g in row] for row in subgrids]
        grid = join(enhanced_subgrids)

      return counton(grid)


    def solve2(self, input: Input) -> Any:
      grid = pattern_to_grid(START)

      def cenhance(g: Grid) -> Grid:
        return cacheable_enhance(tuple(tuple(row) for row in g))

      @functools.cache
      def cacheable_enhance(g: Tuple[Tuple[bool]]) -> Grid:
        return enhance(g, input)

      for step in tqdm(range(18 if len(input) > 2 else 2)):
        if DEBUG:
          print(f'Step {step}: ({counton(grid)}): Grid')
          print(pgrid(grid, sep="\n"))

        if len(grid) % 2 == 0:
          subgrids = split(grid, 2)
        else:
          subgrids = split(grid, 3)

        enhanced_subgrids = [[cenhance(g) for g in row] for row in subgrids]
        grid = join(enhanced_subgrids)

      return counton(grid)

if __name__ == '__main__':
    Day21().main()
