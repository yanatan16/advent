from typing import *
from advent.lib import *

class Button(NamedTuple):
  name: str
  x: int
  y: int

class Prize(NamedTuple):
  x: int
  y: int

class Machine(NamedTuple):
  a: Button
  b: Button
  prize: Prize

Input = List[Machine]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = UtilityParsers.integer
  name = p.reg(r'[A-Z]')
  button = (p.lit('Button') >> name << p.lit(':')) & (p.lit('X') >> n << p.lit(',')) & (p.lit('Y') >> n) > (lambda trip: Button(*trip))
  prize = p.lit('Prize:') >> (p.lit('X=') >> n << p.lit(',')) & (p.lit('Y=') >> n) > (lambda pair: Prize(*pair))
  machine = p.repsep(button, '\n', min=2, max=2) & (p.lit('\n') >> prize) > (lambda pair: Machine(a=pair[0][0], b=pair[0][1], prize=pair[1]))
  input = p.repsep(machine, '\n\n')

class Day13(Advent[Input]):
    year = 2024
    day = 13

    samples = [
'''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    
    # a*ax+b*bx = PX
    # a*ay+b*by = PY
    # x*a+y*b = c
    # x*d+y*e = f

    def tokens_to_solve(self, machine: Machine, max_presses: int | None = 100) -> int | None:
      denominator = (machine.a.x * machine.b.y) - (machine.b.x * machine.a.y)
      if denominator == 0:
        self._print(f'no possible solve {machine}')
        return None

      a = (machine.prize.x * machine.b.y - machine.b.x * machine.prize.y) / denominator
      b = (machine.a.x * machine.prize.y - machine.prize.x * machine.a.y) / denominator

      if a != int(a) or b != int(b) or (max_presses and (a > max_presses or b > max_presses)):
        return None

      return 3 * a + b


    # Second pass
    def tokens_to_solve_using_helper(self, machine: Machine, max_presses: int | None = 100) -> int | None:
      a, b = solve_soe_linear_2var(machine.a.x, machine.b.x, machine.prize.x,
                                   machine.a.y, machine.b.y, machine.prize.y)


      if not a or not b or a != int(a) or b != int(b) or (max_presses and (a > max_presses or b > max_presses)):
        return None

      return 3 * int(a) + int(b)

    def solve1(self, input: Input) -> Any:
      return sum(
        self.tokens_to_solve_using_helper(machine) or 0
        for machine in input
      )

    def solve2(self, input: Input) -> Any:
      prizeadd = 10000000000000
      return sum(
        self.tokens_to_solve_using_helper(
          Machine(machine.a, machine.b, Prize(machine.prize.x + prizeadd, machine.prize.y+prizeadd)),
          max_presses=None
        ) or 0
        for machine in input
      )

if __name__ == '__main__':
    Day13().main()
