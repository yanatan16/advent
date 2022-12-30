# Advent of Code 2022 Day 21
import sys
from typing import *
from dataclasses import dataclass
import enum
from functools import reduce

class OpType(enum.Enum):
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'

    def evaluate(self, left, right):
        if self == OpType.addition:
            return left + right
        elif self == OpType.subtraction:
            return left - right
        elif self == OpType.multiplication:
            return left * right
        elif self == OpType.division:
            return int(left / right)

    def invert(self, left=None, right=None, outcome=None):
        if left is not None:
            if self == OpType.addition:
                return outcome - left
            elif self == OpType.subtraction:
                return -(outcome - left)
            elif self == OpType.multiplication:
                return int(outcome / left)
            elif self == OpType.division:
                return int(left / outcome)
        else:
            if self == OpType.addition:
                return outcome - right
            elif self == OpType.subtraction:
                return outcome + right
            elif self == OpType.multiplication:
                return int(outcome / right)
            elif self == OpType.division:
                return right * outcome

class Operation(NamedTuple):
    left: str
    right: str
    optype: OpType

    @staticmethod
    def parse(raw: str) -> 'Operation':
        left, optype, right = raw.split(' ')
        return Operation(left, right, OpType(optype))

@dataclass
class Monkey:
    name: str
    literal: Optional[int]
    operation: Optional[Operation]

    @staticmethod
    def parse(raw: str) -> 'Monkey':
        name, statement = raw.split(': ')

        try:
            return Monkey(name=name, literal=int(statement), operation=None)
        except:
            return Monkey(name=name, literal=None, operation=Operation.parse(statement))

@dataclass
class Input:
    monkeys: List[Monkey]

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        monkeys=[
            Monkey.parse(line) for line in raw.splitlines()
        ]
    )

def part1(input: Input) -> Output:
    monkeymap = {monkey.name: monkey for monkey in input.monkeys}

    def calc(monkey):
        if monkey.literal:
            return monkey.literal
        else:
            op = monkey.operation
            left = calc(monkeymap[op.left])
            right = calc(monkeymap[op.right])
            return op.optype.evaluate(left, right)

    return calc(monkeymap['root'])

def part2(input: Input) -> Output:
    monkeymap = {monkey.name: monkey for monkey in input.monkeys}

    def calc(monkey):
        if monkey.name == 'humn':
            raise Exception('human found')
        elif monkey.literal:
            return monkey.literal
        else:
            op = monkey.operation
            left = calc(monkeymap[op.left])
            right = calc(monkeymap[op.right])
            return op.optype.evaluate(left, right)

    root = monkeymap['root']

    try:
        target_value = calc(monkeymap[root.operation.left])
        alg_name = root.operation.right
    except:
        target_value = calc(monkeymap[root.operation.right])
        alg_name = root.operation.left

    while alg_name != 'humn':
        monkey = monkeymap[alg_name]
        assert monkey.literal is None
        try:
            sub_target_value = calc(monkeymap[monkey.operation.left])
            alg_name = monkey.operation.right
            target_value = monkey.operation.optype.invert(
                left=sub_target_value,
                outcome=target_value
            )
        except:
            sub_target_value = calc(monkeymap[monkey.operation.right])
            alg_name = monkey.operation.left
            target_value = monkey.operation.optype.invert(
                right=sub_target_value,
                outcome=target_value
            )

    return target_value


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
