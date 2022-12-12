# Advent of Code 2022 Day 9
import sys
from typing import *
from dataclasses import dataclass

Position = Tuple[int, int] # horizontal, vertical
start: Position = (0, 0)

Instruction = Tuple[str, int]

@dataclass
class Input:
    instructions: List[Instruction]

Output = int

def parse_input(raw: str) -> Input:
    def to_instruction(line: str) -> Instruction:
        dir, length = line.split(' ')
        return (dir, int(length)) 
    return Input(
        instructions=[
            to_instruction(line) for line in raw.splitlines()
        ]
    )

@dataclass
class State:
    head: Position
    tail: Position
    visited: Set[Position]

def move(x: Position, direction: str) -> Position:
    if direction == 'R':
        return (x[0] + 1, x[1])
    elif direction == 'L':
        return (x[0] - 1, x[1])
    elif direction == 'U':
        return (x[0], x[1] + 1)
    elif direction == 'D':
        return (x[0], x[1] - 1)
    return x

def is_touching(a: Position, b: Position) -> bool:
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1

def move_to_touch(a: Position, b: Position) -> Position:
    if is_touching(a, b):
        return b

    if a[0] == b[0]:
        xmod = 0
        ymod = int((a[1] - b[1]) / abs(a[1] - b[1]))
    elif a[1] == b[1]:
        xmod = int((a[0] - b[0]) / abs(a[0] - b[0]))
        ymod = 0
    else:
        xmod = int((a[0] - b[0]) / abs(a[0] - b[0]))
        ymod = int((a[1] - b[1]) / abs(a[1] - b[1]))


    return (b[0] + xmod, b[1] + ymod)

def step(state: State, direction: str) -> State:
    new_head = move(state.head, direction)
    new_tail = move_to_touch(new_head, state.tail)

    return State(
        head=new_head,
        tail=new_tail,
        visited=state.visited.union([new_tail])
    )

def part1(input: Input) -> Output:
    state = State(head=(0,0), tail=(0,0), visited=set([(0,0)]))
    for direction, magnitude in input.instructions:
        for i in range(magnitude):
            state = step(state, direction)

    return len(state.visited)

@dataclass
class State2:
    head: Position
    knots: List[Position] # length 9
    visited: Set[Position]

def step2(state: State2, direction: str) -> State2:
    new_head = move(state.head, direction)

    new_knots = []
    for knot in state.knots:
        prev_knot = new_head if len(new_knots) == 0 else new_knots[-1]
        new_knots += [move_to_touch(prev_knot, knot)]

    return State2(
        head=new_head,
        knots=new_knots,
        visited=state.visited.union([new_knots[-1]])
    )

def part2(input: Input) -> Output:
    state = State2(head=(0,0), knots=[(0,0) for i in range(9)], visited=set([(0,0)]))
    for direction, magnitude in input.instructions:
        for i in range(magnitude):
            state = step2(state, direction)

    return len(state.visited)

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
