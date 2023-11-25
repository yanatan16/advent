from typing import *
from dataclasses import dataclass
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

Component = Tuple[int, int]
Input = List[Component]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  component = (UtilityParsers.integer << p.lit('/')) & UtilityParsers.integer > (lambda pair: tuple(pair))
  input = p.repsep(component, '\n')

class Day24(Advent[Input]):
    day = 24

    samples = [
'''0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      assert len(set(input)) == len(input)

      def possibilities(connector: int, rest: Set[Component]) -> List[Component]:
        return [c for c in rest if connector in c]

      def dfs(connector: int, rest: Set[Component]) -> int:
        posses = possibilities(connector, rest)
        if len(posses):
          return max(
            sum(poss) + dfs(poss[0] if poss[1] == connector else poss[1], rest - {poss})
            for poss in posses
          )
        else:
          return 0

      return dfs(0, set(input))


    def solve2(self, input: Input) -> Any:
      def possibilities(connector: int, rest: Set[Component]) -> List[Component]:
        return [c for c in rest if connector in c]

      def dfs(connector: int, rest: Set[Component]) -> Tuple[(int, int)]:
        best = (0, 0)
        for poss in possibilities(connector, rest):
          comp_power = (1, sum(poss))
          rest_power = dfs(poss[0] if poss[1] == connector else poss[1], rest - {poss})
          power = (comp_power[0] + rest_power[0], comp_power[1] + rest_power[1])
          if power > best:
            best = power

        return best

      return dfs(0, set(input))

if __name__ == '__main__':
    Day24().main()
