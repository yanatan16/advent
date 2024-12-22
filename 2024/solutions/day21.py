from typing import *
from advent.lib import *

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg('[0-9]+A')
  input = p.repsep(line, '\n')

numeric_keypad: Dict[str, twod.Coord] = {k: v[0] for k,v in twod.Coord.freqlist(['789','456', '123',' 0A']).items()}
directional_keypad: Dict[str, twod.Coord] = {k:v[0] for k,v in twod.Coord.freqlist([' ^A','<v>']).items()}

class Day21(Advent[Input]):
    year = 2024
    day = 21

    samples = [
'''029A
980A
179A
456A
379A'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def vec2dirs(self, p1: twod.Coord, p2: twod.Coord, avoid: twod.Coord) -> Generator[str, None, None]:
      if p1.x == p2.x:
        yield ('>' if p1.y < p2.y else '<') * abs(p1.y-p2.y)
      elif p1.y == p2.y:
        yield ('v' if p1.x < p2.x else '^') * abs(p1.x-p2.x)
      else:
        corner1 = twod.Coord(p1.x, p2.y)
        corner2 = twod.Coord(p2.x, p1.y)
        if corner1 != avoid:
          for dir1 in self.vec2dirs(p1, corner1, avoid):
            for dir2 in self.vec2dirs(corner1, p2, avoid):
              yield dir1 + dir2
        if corner2 != avoid:
          for dir1 in self.vec2dirs(p1, corner2, avoid):
            for dir2 in self.vec2dirs(corner2, p2, avoid):
              yield dir1 + dir2

    @functools.cache
    def vector_to_dirkeys(self, p1: twod.Coord, p2: twod.Coord, avoid: twod.Coord) -> List[str]:
       return [dir + 'A' for dir in self.vec2dirs(p1, p2, avoid)]

    def unwrap_dirkeys(self, keys: str, keypad: Dict[str, twod.Coord]) -> Generator[str, None, None]:
      vectors = [
        (keypad[fromkey], keypad[tokey])
        for fromkey, tokey in zip('A'+keys[:-1], keys)
      ]
      avoid = keypad[' ']

      poss = [list(self.vector_to_dirkeys(p1, p2, avoid)) for p1, p2 in vectors]
      for px in itertools.product(*poss):
        yield ''.join(px)

    def optimal(self, line: str, layers: int = 3) -> str:
      dkset = set(self.unwrap_dirkeys(line, numeric_keypad))
      for loop in range(layers - 1):
        minlen = min(len(dkeys) for dkeys in dkset)
        dkset = {dkeys for dkeys in dkset if len(dkeys) == minlen}

        dkset = {
          dkeys2
          for dkeys in dkset
          for dkeys2 in self.unwrap_dirkeys(dkeys, directional_keypad)
        }

      return min(dkset, key=lambda dkeys: len(dkeys))

    def solve1(self, input: Input) -> Any:
      return sum(
        int(line[:-1]) * len(self.optimal(line))
        for line in input
      )

    @functools.cache
    def cost(self, fromkey: str, tokey: str, layers: int = 25, numeric: bool = True) -> int:
      keypad = numeric_keypad if numeric else directional_keypad
      ways = list(self.vector_to_dirkeys(
        keypad[fromkey], keypad[tokey], keypad[' ']
      ))
      # self._print(f'cost {fromkey} to {tokey} has {len(ways)} ways with {min(len(way) for way in ways)} length: {ways}')

      if layers == 0:
        return min(len(keys) for keys in ways)

      return min(
        sum(
          self.cost(fk, tk, layers - 1, numeric=False)
          for fk, tk in zip('A' + keys[:-1], keys)
        )
        for keys in ways
      )

    def solve2(self, input: Input) -> Any:
      if self._verbose:
        for line in input:
          cost3 = sum(
            self.cost(fk, tk, layers=2, numeric=True)
            for fk, tk in zip('A' + line[:-1], line)
          )
          self._print(f'line {line}: cost3 {cost3}')

      return sum(
        int(line[:-1]) * sum(
          self.cost(fk, tk)
          for fk, tk in zip('A' + line[:-1], line)
        )
        for line in input
      )


if __name__ == '__main__':
    Day21().main()
