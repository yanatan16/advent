# Advent of Code 2022 Day 8
import sys
from typing import *
from dataclasses import dataclass
from functools import reduce

Grid = List[List[int]]
Loc = Tuple[int,int]

@dataclass
class Input:
    grid: Grid

    def all_locations(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                yield (i,j)

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        grid=[
            [int(n) for n in line]
            for line in raw.splitlines()
        ]
    )

def is_visible(grid: Grid, loc: Loc) -> bool:
    i,j = loc
    value = grid[i][j]
    left = grid[i][:j]
    right = grid[i][(j+1):]
    up = [row[j] for row in grid[:i]]
    down = [row[j] for row in grid[(i+1):]]

    lines = [left, right, up, down]
    lines.sort(key=lambda line: len(line))

    for line in lines:
        if all(v < value for v in line):
            return True
    return False

def part1(input: Input) -> Output:
    return sum(
        1 if is_visible(input.grid, loc) else 0
        for loc in input.all_locations()
    )

def scenic_line_score(height: int, line: int):
    count = 0
    for other_height in line:
        count += 1
        if other_height >= height:
            break
    return count

def scenic_score(grid: Grid, loc: Loc) -> int:
    i,j = loc
    value = grid[i][j]
    left = (grid[i][:j])[::-1]
    right = grid[i][(j+1):]
    up = [row[j] for row in grid[:i]][::-1]
    down = [row[j] for row in grid[(i+1):]]

    lines = [left, right, up, down]

    scores = [
        scenic_line_score(value, line)
        for line in lines
    ]

    return reduce(lambda total, score: total * score, scores, 1)


def part2(input: Input) -> Output:
    return max(*[scenic_score(input.grid, loc) for loc in input.all_locations()])

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
