# Advent of Code 2022 Day 20
import sys
from typing import *
from dataclasses import dataclass
import enum

@dataclass
class Input:
    numbers: List[int]

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        numbers=[
            int(line) for line in raw.splitlines()
        ]
    )

def move_index(i, origin, dest):
    if i == origin:
        return dest
    elif i < origin and i < dest:
        return i
    elif dest <= i < origin:
        return i + 1
    elif origin < i <= dest:
        return i - 1
    elif i > origin and i > dest:
        return i
    else:
        assert False, 'shouldnt get here'

def mix(ns: List[int], times=1) -> List[int]:
    length = len(ns)
    indices = list(range(length))
    ns = [n for n in ns]

    for time in range(times):
        for i in range(length):
            origin = indices[i]
            n = ns[origin]
            dest = (origin + n) % (length - 1)

            ns = ns[:origin] + ns[(origin+1):]
            ns = ns[:dest] + [n] + ns[dest:]

            indices = [move_index(i, origin, dest) for i in indices]

    return ns

def part1(input: Input) -> Output:
    # print(input.numbers)
    mixed = mix(input.numbers)
    # print(mixed)

    zero = mixed.index(0)
    coords = [mixed[(zero + idx) % len(mixed)] for idx in (1000, 2000, 3000)]
    # print(zero)
    # print(coords)

    return sum(coords)

decryption_key: int = 811589153

def part2(input: Input) -> Output:
    premix = [decryption_key * n for n in input.numbers]
    mixed = mix(premix, times=10)

    zero = mixed.index(0)
    coords = [mixed[(zero + idx) % len(mixed)] for idx in (1000, 2000, 3000)]
    return sum(coords)

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
