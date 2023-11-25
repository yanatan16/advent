from typing import *
from solutions2017.lib import Advent
from dataclasses import dataclass
import itertools, collections, functools

from parsita import *


class Pipe(NamedTuple):
    id: int
    comms: List[int]

class Parsers(ParserContext, whitespace=r'[ \t]*'):
    integer = reg(r'[-+]?[0-9]+') > int
    comms = repsep(integer, ',', max=100)
    pipe = ((integer << lit('<->')) & comms) > (lambda pair: Pipe(pair[0], pair[1]))
    

Input = List[Pipe]

class Day12(Advent[Input]):
    day = 12

    samples = [
'''0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5'''
    ]

    def parse(self, raw: str) -> Input:
        lines = raw.strip().splitlines()
        return [Parsers.pipe.parse(s).unwrap() for s in lines]

    def travel_group(self, start: int, commsmap: Dict[int, List[int]]) -> Set[int]:
        seen = set()
        untraveled = {start}

        while len(untraveled) > 0:
            node = untraveled.pop()
            seen.add(node)

            for n in commsmap[node]:
                if n not in seen:
                    untraveled.add(n)

        return seen

    def solve1(self, input: Input) -> Any:
        commsmap = {pipe.id: pipe.comms for pipe in input}
        return len(self.travel_group(0, commsmap))

    def solve2(self, input: Input) -> Any:
        commsmap = {pipe.id: pipe.comms for pipe in input}
        allnodes = set(commsmap.keys())
        groups = []

        while len(allnodes) > 0:
            group = self.travel_group(allnodes.pop(), commsmap)
            groups += [group]
            allnodes = allnodes.difference(group)

        return len(groups)

if __name__ == '__main__':
    Day12().main()
