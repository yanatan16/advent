from typing import *
from solutions2023.lib import *

Input = Tuple[List[int], List[int]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  numbers = p.rep(UtilityParsers.integer)
  time = p.lit('Time:') >> numbers
  distance = p.lit('Distance:') >> numbers
  input = (time << p.lit('\n')) & distance

def ways_to_win(t: int, d: int) -> int:
  return sum(
    1 if hold * (t - hold) > d else 0
    for hold in range(t+1)
  )

def ways_to_win_math(t: int, d: int) -> int:
  detsqrt = math.sqrt(t**2 - 4*d)
  bigroot = (t + detsqrt) / 2
  smallroot = (t - detsqrt) / 2

  if int(smallroot) == smallroot:
    return int(bigroot) - int(smallroot) - 1

  return int(bigroot) - int(smallroot)

class Day6(Advent[Input]):
    year = 2023
    day = 6

    samples = [
'''Time:      7  15   30
Distance:  9  40  200'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      time, distance = input

      total = 1

      for t, d in zip(time,distance):
        total *= ways_to_win_math(t,d)

      return total

    def solve2(self, input: Input) -> Any:
      t = int(''.join(str(t) for t in input[0]))
      d = int(''.join(str(d) for d in input[1]))

      return ways_to_win_math(t, d)

if __name__ == '__main__':
    Day6().main()
