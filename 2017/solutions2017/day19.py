from typing import *
from dataclasses import dataclass
from enum import Enum
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *
import re


Input = List[List[str]]

class Day19(Advent[Input]):
    day = 19

    samples = [
'''     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
'''
    ]

    def parse(self, raw: str) -> Input:
        return [[c for c in line] for line in raw.strip('\n').splitlines()]

    def solve1(self, map: Input) -> Any:
      start = map[0].index('|')
      letters = []

      pos = twod.Coord(0, start)
      dir: Literal['down', 'up', 'right', 'left'] = 'down'
      step = 0

      while True:
        match pos.get(map):
          case None:
            raise RuntimeError(f'Position moved off the map: {pos}')
          case ' ':
            return (''.join(letters), step)
          case '|' | '-':
            pass
          case '+':
            match dir:
              case 'down' | 'up':
                if pos.right().get(map) not in (None, ' '):
                  dir = 'right'
                else:
                  dir = 'left'
              case 'left' | 'right':
                if pos.up().get(map) not in (None, ' '):
                  dir = 'up'
                else:
                  dir = 'down'
          case letter:
            assert re.match(r'[A-Za-z]', letter), f'Letter is not a letter {letter}'
            letters += [letter]

        step += 1
        pos = pos.move(dir)

    def solve2(self, input: Input) -> Any:
        return 'See Part 1'

if __name__ == '__main__':
    Day19().main()
