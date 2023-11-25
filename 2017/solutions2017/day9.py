from typing import *
from solutions2017.lib import Advent
from dataclasses import dataclass
import itertools, collections, functools

from parsita import *

class Parsers(ParserContext, whitespace=r'[ \t]*'):
    cancelled = reg(r'!.') > (lambda _: '')
    garbage_start = lit('<')
    garbage_end = lit('>')
    garbage_inner = cancelled | reg('[^!>]')
    garbage = garbage_start >> rep(garbage_inner) << garbage_end

    group_start = lit('{')
    group_end = lit('}')
    group_inner = group | garbage
    group = group_start >> repsep(group_inner, ',') << group_end

    line = group | garbage



Input = str | List['Input']

class Day9(Advent[Input]):
    day = 9

    samples = [
        '{}',
        '{{{}}}',
        '<random characters>',
        '{{<a!>},{<a!>},{<a!>},{<ab>}}',
        '<{o"i!a,<{i<a>'
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.line.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
        def score(groups, base=1):
            #print('score', groups, base)
            if not isinstance(groups, list):
                return 0

            return base + sum(score(group, base=base+1) for group in groups)

        return score(input)

    def solve2(self, input: Input) -> Any:
        def score(groups):
            if isinstance(groups, str):
                return len(groups)
            return sum(score(g) for g in groups)

        return score(input)

if __name__ == '__main__':
    Day9().main()
