# Advent of Code 2022 Day 2
import sys
from typing import List, Tuple, Dict

Input = List[Tuple[str,str]]

outcome_score: Dict[Tuple[str, str], int] = {
    ('A', 'X'): 3,
    ('B', 'Y'): 3,
    ('C', 'Z'): 3,
    ('A', 'Y'): 6,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('C', 'Y'): 0
}

our_play_score = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

def score(round: Tuple[str, str]) -> int:
    return outcome_score[round] + our_play_score[round[1]]

what_to_play: Dict[Tuple[str, str], str] = {
    ('A', 'X'): 'Z',
    ('B', 'X'): 'X',
    ('C', 'X'): 'Y',

    ('A', 'Y'): 'X',
    ('B', 'Y'): 'Y',
    ('C', 'Y'): 'Z',

    ('A', 'Z'): 'Y',
    ('B', 'Z'): 'Z',
    ('C', 'Z'): 'X',
}

def part2_calculate_what_to_play(round: Tuple[str, str]) -> Tuple[str, str]:
    return (round[0], what_to_play[round])

def parse_input(raw: str) -> Input:
    to_tuple = lambda pair: (pair[0], pair[1])
    return [
        to_tuple(line.split(' ')) for line in raw.splitlines()
    ]

def part1(input: Input) -> int:
    return sum(score(round) for round in input)

def part2(input: Input) -> int:
    return sum(
        score(part2_calculate_what_to_play(round))
        for round in input
    )

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])

