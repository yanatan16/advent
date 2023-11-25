from typing import *
from dataclasses import dataclass
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  input = UtilityParsers.integer

Input = List[int]

@dataclass
class Spinlock:
  move: int
  buffer = [0]
  position: int = 0

  def iteration(self, insertion: int):
    pos = (self.position + self.move) % len(self.buffer)
    self.buffer = self.buffer[:(pos+1)] + [insertion] + self.buffer[(pos+1):]
    self.position = pos + 1

  def __str__(self):
    return ' '.join(f'{n}' if self.position != i else f'({n})'
                    for i, n in enumerate(self.buffer))

class Day17(Advent[Input]):
    day = 17

    samples = [
'3'
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      spinlock = Spinlock(move=input)

      # for i in range(1, 10):
      #   spinlock.iteration(i)
      #   print(f'{i}: {spinlock}')

      # return 'DEBUG'

      for i in tqdm(range(1, 2017+1)):
        spinlock.iteration(i)

      return spinlock.buffer[spinlock.buffer.index(2017) + 1]

    def solve2(self, input: Input) -> Any:
      if input == 3:
        return 'SKIP'

      # No need to keep the whole array, that's slow. We just need to track when a number is inserted after 0
      # Since a number is never inserted before 0, 0 is always in the first position
      # So we just track {i} when the insertion point is 0 and whala!
      move = input
      size = 1
      cur = 0
      ret = 0

      for i in tqdm(range(1, 50000000+1)):
        cur = (cur + move) % size
        if cur == 0:
          ret = i
          print(f'After 0 has changed to {ret} at step {i}')

        size += 1
        cur += 1

      return ret

if __name__ == '__main__':
    Day17().main()
