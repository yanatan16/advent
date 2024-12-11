from typing import *
from advent.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \t\n]*'):
  n = UtilityParsers.integer
  line = p.rep(n)
  input = line

class Day11(Advent[Input]):
    year = 2024
    day = 11

    samples = [
      '125 17',
'''
0 1 10 99 999
'''
    ]

    @staticmethod
    def blink1(stone: int) -> List[int]:
      if stone == 0:
        return [1]
      elif len(str(stone)) % 2 == 0:
        ss = str(stone)
        p1, p2 = ss[:(len(ss)//2)], ss[(len(ss)//2):]
        return [int(p1), int(p2)]
      else:
        return [2024 * stone]

    @staticmethod
    def blink(stones: List[int]) -> List[int]:
      return [
        s
        for stone in stones
        for s in Day11.blink1(stone)
      ]

    def parse(self, raw: str) -> Input:
      return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      state = input
      for i in range(25):
        self._print(f"After {i} blinks, we have {len(state)} stones: {state[:25]}")
        state = self.blink(state)

      return len(state), len(set(state))

    @staticmethod
    def blinkfreqs(stones: Dict[int, int]) -> Dict[int, int]:
      newstones = {}
      for stone, count in stones.items():
        for s in Day11.blink1(stone):
          newstones[s] = newstones.get(s, 0) + count

      return newstones

    def solve2(self, input: Input) -> Any:
      if len(input) < 6:
        return -1

      state = freqs(input)
      for i in tqdm(range(75)):
        state = self.blinkfreqs(state)

      return sum(state.values())

if __name__ == '__main__':
    Day11().main()
