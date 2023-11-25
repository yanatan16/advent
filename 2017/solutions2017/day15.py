from typing import *
from dataclasses import dataclass
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  gen_a = p.lit('Generator A starts with') >> UtilityParsers.integer
  gen_b = p.lit('Generator B starts with') >> UtilityParsers.integer
  input = gen_a & (UtilityParsers.newline >> gen_b)

Input = List[int]

A_FACTOR = 16807
B_FACTOR = 48271
DIVISOR = 2147483647
TWO_SIXTEEN = 2**16

@dataclass
class Generator:
  prev: int
  factor: int
  divisor: int = DIVISOR

  multiples: int | None = None

  def next(self):
    x = (self.prev * self.factor) % self.divisor

    while self.multiples is not None and x % self.multiples != 0:
      x = (x * self.factor) % self.divisor

    self.prev = x
    return x

class Day15(Advent[Input]):
    day = 15

    samples = [
'''Generator A starts with 65
Generator B starts with 8921'''
    ]

    def parse(self, raw: str) -> Input:
      return Parsers.input.parse(raw.strip()).unwrap()

    def low16_match(self, x: int, y: int) -> bool:
      return x % TWO_SIXTEEN == y % TWO_SIXTEEN

    def solve1(self, input: Input) -> Any:
      start_a, start_b = input
      a = Generator(prev=start_a, factor=A_FACTOR)
      b = Generator(prev=start_b, factor=B_FACTOR)

      count = 0
      last = -1

      for step in tqdm(range(40000000)):
        if self.low16_match(a.next(), b.next()):
          last = step
          count += 1

      return count

    def solve2(self, input: Input) -> Any:
      start_a, start_b = input
      a = Generator(prev=start_a, factor=A_FACTOR, multiples=4)
      b = Generator(prev=start_b, factor=B_FACTOR, multiples=8)

      count = 0

      for step in tqdm(range(5000000)):
        if self.low16_match(a.next(), b.next()):
          count += 1

      return count

if __name__ == '__main__':
    Day15().main()
