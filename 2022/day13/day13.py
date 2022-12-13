# Advent of Code 2022 Day 13
import sys
from typing import *
from dataclasses import dataclass
from itertools import zip_longest
from functools import cmp_to_key

Packet = Union[int, List['Packet']]

@dataclass
class Input:
    pairs: Tuple[Packet, Packet]

Output = int

def parse_input(raw: str) -> Input:
    def to_pair(lines: str) -> Tuple[Packet, Packet]:
        first, second = lines.splitlines()
        return (eval(first), eval(second))

    return Input(
        pairs=[
            to_pair(line) for line in raw.split('\n\n')
        ]
    )

def right_order(left: Packet, right: Packet) -> Optional[bool]:
    if type(left) is int and type(right) is int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    elif type(left) is list and type(right) is int:
        return right_order(left, [right])
    elif type(left) is int and type(right) is list:
        return right_order([left], right)
    else:
        for left_value, right_value in zip_longest(left, right, fillvalue=None):
            if left_value is None:
                return True
            elif right_value is None:
                return False
            else:
                compare = right_order(left_value, right_value)
                if compare is not None:
                    return compare
        return None

def part1(input: Input) -> Output:
    sum = 0
    for i, pair in enumerate(input.pairs):
        if right_order(*pair):
            sum += i + 1
    return sum

def right_order_compare(left: Packet, right: Packet) -> int:
    compare = right_order(left, right)
    if compare == True:
        return -1
    elif compare == False:
        return 1
    else:
        return 0

def part2(input: Input) -> Output:
    key = cmp_to_key(right_order_compare)

    packets = [
        [[2]],
        [[6]],
    ] + [packet for pair in input.pairs for packet in pair]

    packets.sort(key=key)

    div_2: int = 0
    div_6: int = 0

    for i, packet in enumerate(packets):
        if packet == [[2]]:
            div_2 = i+1
        elif packet == [[6]]:
            div_6 = i+1

    return div_2 * div_6

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
