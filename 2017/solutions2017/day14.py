from typing import *
from dataclasses import dataclass
import itertools, collections, functools
from parsita import *
from solutions2017.lib import *

from .knothash import KnotHash

class Parsers(ParserContext, whitespace=r'[ \t]*'):
  input = UtilityParsers.name

Input = List[int]

class Day14(Advent[Input]):
    day = 14

    samples = [
'''flqrgnkx'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
        knothash = KnotHash()

        return sum(
            sum(1 if bit else 0
                for bit in knothash.hash(f'{input}-{i}', format='binary'))
            for i in range(128)
            )

    def solve2(self, input: Input) -> Any:
        knothash = KnotHash()

        map = [
            knothash.hash(f'{input}-{i}', format='binary')
            for i in range(128)
        ]

        assert len(map[0]) == 128, f'map[0] is len {len(map[0])}'

        seen = set()
        regioncount = 0

        def connected(coord: twod.Coord) -> List[twod.Coord]:
            return [
                neighbor for neighbor in coord.neighbors()
                if neighbor.get(map) == True
            ]

        for coord in twod.Coord.all_coords(len(map), len(map[0])):
            if coord not in seen and coord.get(map) == True:
                region = walk(coord, connected)
                regioncount += 1
                seen = seen | region

        return regioncount


if __name__ == '__main__':
    Day14().main()
