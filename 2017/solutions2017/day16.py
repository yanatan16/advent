from typing import *
from dataclasses import dataclass
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

class Spin(NamedTuple):
  x: int

class Exchange(NamedTuple):
  a: int
  b: int

class Partner(NamedTuple):
  a: str
  b: str

DanceMove = Spin | Exchange | Partner
Input = List[DanceMove]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  spin = (p.lit('s') >> UtilityParsers.integer) > (lambda x: Spin(x))
  exchange = (p.lit('x') >> UtilityParsers.integer) & (p.lit('/') >> UtilityParsers.integer) > (lambda pair: Exchange(*pair))
  partner = (p.lit('p') >> UtilityParsers.char) & (p.lit('/') >> UtilityParsers.char) > (lambda pair: Partner(*pair))

  dancemove = spin | exchange | partner

  input = p.repsep(dancemove, ',')

class Dance:
  dancers: List[str]

  def __init__(self, size: int):
    self.dancers = [chr(ord('a') + i) for i in range(size)]

  def move(self, dm: DanceMove):
    match dm:
      case Spin(x=x):
        self.dancers = self.dancers[-x:] + self.dancers[:-x]
      case Exchange(a=a, b=b):
        self.dancers[a], self.dancers[b] = self.dancers[b], self.dancers[a]
      case Partner(a=a, b=b):
        self.move(Exchange(a=self.dancers.index(a), b=self.dancers.index(b)))

  def __str__(self) -> str:
    return ''.join(self.dancers)

class Day16(Advent[Input]):
    day = 16

    samples = [
'''s1,x3/4,pe/b'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      dance = Dance(5 if len(input) == 3 else 16)

      for move in input:
        dance.move(move)

      return dance

    def solve2(self, input: Input) -> Any:
      dance = Dance(5 if len(input) == 3 else 16)

      orders: Dict[str, int] = {}

      for step in range(1000000000):
        if str(dance) in orders:
          before = orders[str(dance)]
          repeat_steps = step - before
          break

        orders[str(dance)] = step
        for move in input:
          dance.move(move)

      invorders = {step: order for order, step in orders.items()}

      return invorders[1000000000 % repeat_steps]

if __name__ == '__main__':
    Day16().main()
