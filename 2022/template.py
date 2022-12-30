# Advent of Code 2022 Day XX
import sys
from typing import *
from dataclasses import dataclass
import enum
from functools import reduce


@dataclass
class Input:
    lines: List[str]

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        lines=[
            line for line in raw.splitlines()
        ]
    )

def part1(input: Input) -> Output:
    return -1

def part2(input: Input) -> Output:
    return -1

def main(input_file, skip=None):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    if skip != 'skip':
        print('Part 1:', part1(input))
    else:
        print('Skipping Part 1')
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(*sys.argv[1:])
