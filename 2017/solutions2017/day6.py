from typing import *
from solutions2017.lib import Advent

Input = List[int]

class Day6(Advent[Input]):
    day = 6

    samples = [
'0 2 7 0'
    ]

    def parse(self, raw: str) -> Input:
        return [int(s) for s in raw.strip().split()]

    def solve1(self, input: Input, part2 = False) -> Any:
        seen = {}
        cur = tuple(input)

        while cur not in seen:
            seen[cur] = len(seen)

            most, mosti = -1, 0
            for i in range(len(cur)):
                if cur[i] > most:
                    most, mosti = cur[i], i

            mcur = list(cur)
            mcur[mosti] = 0
            for i in range(most):
                index = (mosti + i + 1) % len(mcur)
                mcur[index] += 1

            cur = tuple(mcur)

        return len(seen), len(seen) - seen[cur]


    def solve2(self, input: Input) -> Any:
        return 'See part 1'

if __name__ == '__main__':
    Day6().main()
