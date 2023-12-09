from typing import *
from solutions2023.lib import *

Line = List[int]
Input = List[Line]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = UtilityParsers.integer
  line = p.rep(n)
  input = p.repsep(line, '\n')

def diff(seq: List[int]) -> List[int]:
  return [y-x for x,y in zip(seq, seq[1:])]

def repdiff(seq: List[int]) -> List[List[int]]:
  seqs = [seq]
  while not all(x==0 for x in seqs[-1]):
    seqs += [diff(seqs[-1])]
  return seqs

class Day9(Advent[Input]):
    year = 2023
    day = 9

    samples = [
'''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      def predict_next(seq: List[int]) -> int:
        diffs = repdiff(seq)
        return sum(diff[-1] for diff in diffs)

      return sum(predict_next(seq) for seq in input)

    def solve2(self, input: Input) -> Any:
      def predict_prev(diffs: List[List[int]]) -> int:
        if len(diffs) == 1:
          return 0
        return diffs[0][0] - predict_prev(diffs[1:])

      return sum(predict_prev(repdiff(seq)) for seq in input)

if __name__ == '__main__':
    Day9().main()
