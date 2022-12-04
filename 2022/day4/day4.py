# Advent of Code 2022 Day 04
import sys
from typing import *
from dataclasses import dataclass

@dataclass
class Range:
    low: int
    high: int

    def __init__(self, line: str):
        low, high = line.split('-')
        self.low = int(low)
        self.high = int(high)

    def contains(self, other: Any) -> bool:
        return other.low >= self.low and other.high <= self.high

def range_overlap(a: Range, b: Range) -> bool:
    return a.contains(b) or b.contains(a) or (
        a.low <= b.low <= a.high
    ) or (
        a.low <= b.high <= a.high
    )

@dataclass
class Input:
    ranges: List[Tuple[Range, Range]]

def line_to_ranges(line: str) -> Tuple[Range, Range]:
    first, second = line.split(',')
    return Range(first), Range(second)

def parse_input(raw: str) -> Input:
    return Input(
        ranges=[
           line_to_ranges(line) for line in raw.splitlines()
        ]
    )

def part1(input: Input) -> int:
    return sum(
        1 if (
            assignment1.contains(assignment2) or assignment2.contains(assignment1)
        ) else 0
        for assignment1, assignment2 in input.ranges
    )

def part2(input: Input) -> int:
    return sum(
        1 if (
            range_overlap(assignment1, assignment2)
        ) else 0
        for assignment1, assignment2 in input.ranges
    )

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])

