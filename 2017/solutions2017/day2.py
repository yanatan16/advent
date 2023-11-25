
from typing import *
from solutions2017.lib import Advent
from itertools import permutations

Input = List[List[int]]

class Day2(Advent[Input]):
    day = 2

    samples = [
'''5 9 2 8
9 4 7 3
3 8 6 5'''
    ]

    def parse(self, raw: str) -> Input:
        return [[int(s) for s in line.strip().split()]
                for line in raw.strip().splitlines()]

    def solve1(self, input: Input) -> Any:
        return sum(max(row) - min(row) for row in input)

    def even_divide(self, x: int, y: int) -> int | None:
        if x % y == 0:
            return int(x / y)
        if y % x == 0:
            return int(y / x)
    
    def first_event_divide(self, ns: List[int]) -> int:
        for x, y in permutations(ns, 2):
            v = self.even_divide(x, y)
            if v:
                return v
        else:
            raise RuntimeError(f'List of integers did not produce an evenly divisible pair: {ns}')


    def solve2(self, input: Input) -> Any:
        return sum(self.first_event_divide(row) for row in input)

if __name__ == '__main__':
    Day2().main()
