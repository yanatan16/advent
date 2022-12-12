# Advent of Code 2022 Day 10
import sys
from typing import *
from dataclasses import dataclass
import enum

class Command(enum.Enum):
    noop = 'noop'
    addx = 'addx'

@dataclass
class Instruction:
    cmd: Command
    params: [int]

    def __init__(self, line: str):
        cmd_s, *rest = line.split(' ')
        self.cmd = Command(cmd_s)
        self.params = [int(p) for p in rest]

    def __str__(self):
        return ' '.join([self.cmd.value] + [str(p) for p in self.params])

@dataclass
class Input:
    program: List[Instruction]

Output = int

class Device:
    X:int = 1
    Y:int = 1
    cycle: int = 0

    signal_strength: List[int] = []

    def increment_cycle(self):
        self.cycle += 1

        if (self.cycle - 20) % 40 == 0:
            self.signal_strength += [self.X * self.cycle]

        self.draw()

    def execute(self, inst: Instruction):
        print(inst)
        if inst.cmd == Command.noop:
            self.increment_cycle()
        elif inst.cmd == Command.addx:
            self.increment_cycle()
            self.increment_cycle()

            self.X += inst.params[0]

    ## Part 2
    image: List[List[bool]] = [[False for j in range(40)] for i in range(6)]
    def draw(self):
        cycle = self.cycle - 1
        i = int(cycle / 40)
        j = cycle % 40

        self.image[i][j] = abs(self.X - j) <= 1

    def __str__(self):
        return '\n'.join(
            ''.join('#' if cell else '.' for cell in row)
            for row in self.image
        )

def parse_input(raw: str) -> Input:
    return Input(
        program=[
            Instruction(line) for line in raw.splitlines()
        ]
    )

def part1(input: Input) -> Output:
    device = Device()

    for inst in input.program:
        device.execute(inst)

    print('signal strength', device.signal_strength)

    return sum(device.signal_strength[:6])

def part2(input: Input) -> Output:
    device = Device()

    for inst in input.program:
        device.execute(inst)

    print(device)
    return -1

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
