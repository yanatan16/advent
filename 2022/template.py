# Advent of Code 2022 Day XX
import sys
from typing import List

Input = List[str]

def parse_input(raw: str) -> Input:
    return [
        line for line in raw.splitlines()
    ]

def part1(input: Input) -> int:
    return -1

def part2(input: Input) -> int:
    return -1

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])

