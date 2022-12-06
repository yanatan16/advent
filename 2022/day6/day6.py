# Advent of Code 2022 Day 6
import sys
from typing import *
from dataclasses import dataclass

Datastream = str
@dataclass
class Input:
    stream: Datastream

Output = int

def parse_input(raw: str) -> Input:
    return Input(stream=raw)

def find_first_unique_substring(stream: Datastream, length: int) -> int:
    for i in range(len(stream) - length):
        if length == len(set(stream[i:(i+length)])):
            return i+length

    return -1

def part1(input: Input) -> Output:
    return find_first_unique_substring(input.stream, 4)

def part2(input: Input) -> Output:
    return find_first_unique_substring(input.stream, 14)

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
