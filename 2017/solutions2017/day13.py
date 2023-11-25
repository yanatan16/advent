from typing import *
from solutions2017.lib import Advent, UtilityParsers
from dataclasses import dataclass
import itertools, collections, functools

from parsita import *

class Scanner(NamedTuple):
    depth: int
    range: int


class Parsers(ParserContext, whitespace=r'[ \t]*'):
    scanner_t = (UtilityParsers.integer << ':') & UtilityParsers.integer
    scanner = scanner_t > (lambda pair: Scanner(*pair))
    input = repsep(scanner, '\n')

Input = List[Scanner]

class Day13(Advent[Input]):
    day = 13

    samples = [
'''0: 3
1: 2
4: 4
6: 4'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
        def caught(scanner: Scanner) -> bool:
            return scanner.depth % (scanner.range * 2 - 2) == 0

        def severity(scanner: Scanner) -> int:
            return scanner.depth * scanner.range

        return sum(severity(s) for s in input if caught(s))

    def solve2(self, input: Input) -> Any:
        def caught(scanner: Scanner, delay: int) -> bool:
            return (delay + scanner.depth) % (scanner.range * 2 - 2) == 0

        for delay in itertools.count(0):
            if all(not caught(s, delay) for s in input):
                return delay

if __name__ == '__main__':
    Day13().main()
