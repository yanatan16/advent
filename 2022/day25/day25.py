# Advent of Code 2022 Day 25
import sys
from typing import *
from dataclasses import dataclass
import enum
from functools import reduce
from itertools import zip_longest

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

snafu = {
    '-': -1,
    '=': -2,
    '0': 0,
    '1': 1,
    '2': 2
}

snafu_reverse = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2'
}

def snafu_add(left, right):
    sum = [l + r for l, r in zip_longest(left, right, fillvalue=0)] + [0]

    for i in range(len(sum)):
        value = sum[i]
        if value < -2:
            sum[i] += 5
            sum[i+1] -= 1
        elif value > 2:
            sum[i] -= 5
            sum[i+1] += 1

    return sum

def part1(input: Input) -> Output:
    numbers = [[snafu[n] for n in line[::-1]] for line in input.lines]

    current = [0]

    for number in numbers:
        # print(f'Adding {current} and {number}')
        current = snafu_add(current, number)
        # print(f'got {current}')

    return ''.join(snafu_reverse[n] for n in current[::-1]).lstrip('0')

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
