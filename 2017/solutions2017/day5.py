import itertools
from typing import *
from solutions2017.lib import Advent

Input = List[int]

class Day5(Advent[Input]):
    day = 5

    samples = [
'''0
3
0
1
-3'''
    ]

    def parse(self, raw: str) -> Input:
        return [int(s) for s in raw.strip().splitlines()]

    def solve1(self, input: Input) -> Any:
        maze = [j for j in input]
        ptr = 0

        for step in itertools.count(start=0):
            if ptr < 0 or ptr >= len(maze):
                return step

            jump = maze[ptr]

            maze[ptr] += 1

            ptr += jump

    def solve2(self, input: Input) -> Any:
        maze = [j for j in input]
        ptr = 0

        for step in itertools.count(start=0):
            if ptr < 0 or ptr >= len(maze):
                return step

            jump = maze[ptr]

            if jump >= 3:
                maze[ptr] -= 1
            else:
                maze[ptr] += 1

            ptr += jump

if __name__ == '__main__':
    Day5().main()
