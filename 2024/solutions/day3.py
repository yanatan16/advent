from typing import *
from advent.lib import *

class Mul(NamedTuple):
  x: int
  y: int

  @property
  def result(self):
    return self.x * self.y

class Do(NamedTuple):
  pass

class Dont(NamedTuple):
  pass

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg(r'.*')
  input = p.repsep(line, '\n')

class Problem1Parser(p.ParserContext):
  junk = p.reg(r'.') > (lambda _: None)
  mul = (p.lit('mul(') >> p.repsep(UtilityParsers.integer, ',', min=2, max=2) << p.lit(')')) > (lambda ns: Mul(*ns))
  item = mul | junk
  line = p.rep(item) > (lambda items: [item for item in items if item])

class Problem2Parser(p.ParserContext):
  junk = p.reg(r'.')
  n = UtilityParsers.integer
  mul = (p.lit('mul(') >> p.repsep(n, ',', min=2, max=2) << p.lit(')')) > (lambda ns: Mul(*ns))
  do = p.lit('do()') > (lambda _: Do())
  dont = p.lit("don't()") > (lambda _: Dont())
  prob2item = mul | do | dont | junk
  line = p.rep(prob2item)

class Day3(Advent[Input]):
    year = 2024
    day = 3

    samples = [
      """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""",
      """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      parsed = [
        instr
        for line in input
        for instr in Problem1Parser.line.parse(line).unwrap()
        if instr
      ]
      self._print(parsed)

      return sum(
        mul.result
        for mul in parsed
      )

    def solve2(self, input: Input) -> Any:
      instructions = [
        instr
        for line in input
        for instr in Problem2Parser.line.parse(line).unwrap()
        if isinstance(instr, Mul | Do | Dont)
      ]

      enabled = True
      total = 0

      for instr in instructions:
        match instr:
          case Mul(x, y):
            if enabled:
              total += x * y
          case Do():
            enabled = True
          case Dont():
            enabled = False

      return total

if __name__ == '__main__':
    Day3().main()
