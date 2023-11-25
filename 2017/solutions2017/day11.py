from typing import *
from solutions2017.lib import *
from dataclasses import dataclass
import itertools, collections, functools

# from parsita import *

Input = List[hexd.Direction]

class Day11(Advent[Input]):
    day = 11

    samples = [
        'se,sw,se,sw,sw'
    ]

    def parse(self, raw: str) -> Input:
        return raw.strip().split(',')

    def solve1(self, input: Input) -> Any:
        cur = hexd.Coord(0,0,0)

        for dir in input:
            cur = cur.dir(dir)

        return cur.dist()

    def solve2(self, input: Input) -> Any:
        most = 0
        cur = hexd.Coord(0,0,0)

        for dir in input:
            cur = cur.dir(dir)
            most = max([most, cur.dist()])

        return most

if __name__ == '__main__':
    Day11().main()
