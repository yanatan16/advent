
from typing import *
from solutions2017.lib import Advent

Input = List[List[str]]

class Day4(Advent[Input]):
    day = 4

    samples = [

    ]

    def parse(self, raw: str) -> Input:
        return [line.split() for line in raw.strip().splitlines()]

    def solve1(self, input: Input) -> Any:
        return sum(1 for passphrase in input if len(set(passphrase)) == len(passphrase))

    def solve2(self, input: Input) -> Any:
        return self.solve1([
            [''.join(sorted(word)) for word in passphrase]
            for passphrase in input
        ])

if __name__ == '__main__':
    Day4().main()
