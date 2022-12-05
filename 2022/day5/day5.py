# Advent of Code 2022 Day 5
import sys
from typing import *
from dataclasses import dataclass

Crate = str
Stack = List[Crate] #bottom is index 0, top is index len(stack)

@dataclass
class Instruction:
    quantity: int
    from_stack: int #indices
    to_stack: int

@dataclass
class Input:
    stacks: List[Stack]
    procedure: List[Instruction]

def parse_instruction(line: str) -> Instruction:
    move, to = line.split(' from ')
    quantity = move.split(' ')[1]
    from_stack, to_stack = to.split(' to ')
    return Instruction(
        quantity=int(quantity),
        from_stack=int(from_stack) - 1,
        to_stack=int(to_stack) - 1
    )

def parse_stacks(raw: str) -> List[Stack]:
    lines = raw.splitlines()
    columns = len(lines[-1].split('  '))
    stacks = [[] for i in range(columns)]

    for row in lines[-2::-1]:
        for stacki in range(columns):
            prefix = stacki * 4
            crate = row[prefix:(prefix+3)]

            if crate.startswith('[') and crate.endswith(']'):
                stacks[stacki] += [crate[1]]

    return stacks

def parse_input(raw: str) -> Input:
    stacks, procedures = raw.split('\n\n')

    return Input(
        stacks=parse_stacks(stacks),
        procedure=[parse_instruction(line) for line in procedures.splitlines()]
    )

def execute_instruction(stacks: List[Stack], inst: Instruction, reverse=True) -> List[Stack]:
    new_stacks = [stack for stack in stacks]
    crates_moving = stacks[inst.from_stack][(-inst.quantity):]

    if reverse:
        crates_moving = crates_moving[::-1]

    new_stacks[inst.from_stack] = stacks[inst.from_stack][:(-inst.quantity)]
    new_stacks[inst.to_stack] = stacks[inst.to_stack] + crates_moving

    return new_stacks


def part1(input: Input) -> str:
    stacks = input.stacks
    for instruction in input.procedure:
        stacks = execute_instruction(stacks, instruction)

    return ''.join(stack[-1] for stack in stacks if len(stack))

def part2(input: Input) -> str:
    stacks = input.stacks
    for instruction in input.procedure:
        stacks = execute_instruction(stacks, instruction, reverse=False)

    return ''.join(stack[-1] for stack in stacks if len(stack))

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().rstrip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
