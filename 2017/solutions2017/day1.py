from typing import *
from solutions2017.lib import Advent

Input = List[int]

class Day1(Advent[Input]):
    day = 1

    samples = [

    ]

    def parse(self, raw: str) -> Input:
        return [int(s) for s in raw.strip()]

    def solve1(self, input: Input) -> Any:
        return sum(x for x,y in zip(input, input[1:] + [input[0]]) if x == y)

    def solve2(self, input: Input) -> Any:
        step = int(len(input)/2)
        return sum(x for x,y in zip(input, input[step:] + input[:step]) if x == y)

if __name__ == '__main__':
    Day1().main()
