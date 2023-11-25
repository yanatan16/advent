from typing import *
from solutions2017.lib import Advent
from dataclasses import dataclass
import itertools, collections, functools

# from parsita import *

from .knothash import KnotHash

Input = Tuple[List[int], List[int]]

class Day10(Advent[Input]):
    day = 10

    samples = [
        '3,4,1,5',
        '',
        'AoC 2017'
    ]

    def parse(self, raw: str) -> Input:
        return (
            # Part 1 lengths
            [int(s) for s in raw.strip().split(',')] if ',' in raw else [],
            # Part 2 pass string
            raw.strip()
        )

    def solve1(self, input: Input) -> Any:
        lengths, _ = input

        if len(lengths) == 0:
            return 'NA'
        elif len(lengths) < 5:
            final, _, _ = KnotHash()._round(list(range(5)), lengths)
        else:
            final, _, _ = KnotHash()._round(list(range(256)), lengths)

        return final[0] * final[1]

    def solve2(self, input: Input) -> Any:
        _, key = input

        return KnotHash().hash(key)

if __name__ == '__main__':
    Day10().main()
