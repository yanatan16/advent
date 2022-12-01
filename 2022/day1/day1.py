# Advent of Code 2022 Day 1
import sys
from typing import List

def parse_input(raw) -> List[List[int]]:
    return [
        [int(line) for line in section.splitlines()]
        for section in raw.split('\n\n')
    ]

def part1(input: List[List[int]]) -> int:
    totals = [sum(snacks) for snacks in input]
    return max(*totals)

def part2(input: List[List[int]]) -> int:
    totals = [sum(snacks) for snacks in input]
    totals.sort()
    return sum(totals[-3:])

def main(input_file):
    with open(input_file[0]) as f:
        input = parse_input(f.read())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1:])
