from typing import *
from advent.lib import *

Input = List[Tuple[int, List[int]]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#]+')
  n = UtilityParsers.integer
  test = n << p.lit(':')
  line = test & p.rep(n)
  input = p.repsep(line, '\n')

class Day7(Advent[Input]):
    year = 2024
    day = 7

    samples = [
'''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def operations(self, n: int) -> Generator[List[str], None, None]:
      for i in range(2**n):
        yield [
          '*' if i // (2**x) % 2  == 1 else '+'
          for x in range(n)
        ]


    def could_be_true_p1(self, case: Tuple[int, List[int]]) -> bool:
      test, values = case

      for ops in self.operations(len(values) - 1):
        total = values[0]

        for op, val in zip(ops, values[1:]):
          if op == '*':
            total *= val
          else:
            total += val

        if total == test:
          self._print('true', test, ops, values)
          return True

      return False

    def could_be_true_p1_smart(self, case: Tuple[int, List[int]]) -> bool:
      test, values = case

      if len(values) == 1:
        return test == values[0]
      elif test < values[0]:
        return False
      else:
        # + is always an option
        if self.could_be_true_p1_smart((test - values[-1], values[:-1])):
          return True
        elif test % values[-1] == 0: # * is only an option is last value divides test
          return self.could_be_true_p1_smart((test // values[-1], values[:-1]))
        else:
          return False

    def solve1(self, input: Input) -> Any:
      return sum(
        case[0] if self.could_be_true_p1_smart(case) else 0
        for case in input
      )

    def operations_p2(self, n: int) -> Generator[List[str], None, None]:
      for i in range(3**n):
        yield [
          ['+','*','||'][i // (3**x) % 3]
          for x in range(n)
        ]

    def could_be_true_p2(self, case: Tuple[int, List[int]]) -> bool:
      test, values = case

      for ops in self.operations_p2(len(values) - 1):
        total = values[0]

        for op, val in zip(ops, values[1:]):
          if op == '*':
            total *= val
          elif op == '+':
            total += val
          else:
            total = int(str(total) + str(val))

        if total == test:
          self._print('true', test, ops, values)
          return True

      return False


    def could_be_true_p2_smart(self, case: Tuple[int, List[int]]) -> bool:
      test, values = case

      if len(values) == 1:
        return test == values[0]
      elif test < values[0]:
        return False
      else:
        # + is always an option
        v = values[-1]
        if self.could_be_true_p2_smart((test - v, values[:-1])):
          return True
        # * is only an option is last value divides test
        elif test % v == 0 and self.could_be_true_p2_smart((test // v, values[:-1])):
          return True
        elif str(test).endswith(str(v)):
          reduced = int(str(test)[:-(len(str(v)))])
          return self.could_be_true_p2_smart((reduced, values[:-1]))
        else:
          return False

    def solve2(self, input: Input) -> Any:
      return sum(
        case[0] if self.could_be_true_p2_smart(case) else 0
        for case in tqdm(input)
      )

    
if __name__ == '__main__':
    Day7().main()
