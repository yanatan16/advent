from typing import *
from solutions2023.lib import *

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  input = p.repsep(p.reg(r'[a-z0-9A-Z]+'), '\n')

digits = {
  str(n): n
  for n in range(10)
}

digits.update({
  'one': 1,
  'two': 2,
  'three': 3,
  'four': 4,
  'five': 5,
  'six': 6,
  'seven': 7,
  'eight': 8,
  'nine': 9
})

class Day1(Advent[Input]):
    year = 2023
    day = 1

    samples = [
'''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet''',

      '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      digits = [
        [d for d in line if d in '0123456789']
        for line in input
      ]
      return sum(
        int(line[0] + line[-1])
        for line in digits
      )

    def solve2(self, input: Input) -> Any:
      revdigits = {d[::-1]:v for d,v in digits.items()}

      def calib1(line: str, digits=digits):
        i = 0
        while True:
          for d,v in digits.items():
            if line[i:(i+len(d))] == d:
              return v
          i += 1

      def calibrate(line: str):
        return calib1(line)*10 + calib1(line[::-1], digits=revdigits)

      return sum(
        calibrate(line)
        for line in input
      )

if __name__ == '__main__':
    Day1().main()
