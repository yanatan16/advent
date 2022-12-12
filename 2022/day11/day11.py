# Advent of Code 2022 Day 11
import sys
from typing import *
from dataclasses import dataclass
import enum
import tqdm
import time
from functools import cache, reduce

@dataclass
class Test:
    divisible_by: int

    def __init__(self, line: str):
        self.divisible_by = int(line.split(' ')[-1])

    def passes(self, worry: int) -> bool:
        return worry % self.divisible_by == 0


class OperationType(enum.Enum):
    add = '+'
    multiply = '*'

    def calculate(self, left: int, right: int) -> int:
        if self == OperationType.add:
            return left + right
        elif self == OperationType.multiply:
            return left * right

Old = 'old'

@cache
def calculate(left: Union[int, Old], right: Union[int, Old], op_type: OperationType, old: int) -> int:
    xleft = old if left == Old else left
    xright = old if right == Old else right

    return op_type.calculate(xleft, xright)

@dataclass
class Operation:
    left: Union[int, Old]
    right: Union[int, Old]
    op_type: OperationType

    def __init__(self, line: str):
        eqleft, eqright = line.split(' = ')
        assert eqleft == 'new'
        left, middle, right = eqright.split(' ')

        if left == Old:
            self.left = Old
        else:
            self.left = int(left)

        if right == Old:
            self.right = Old
        else:
            self.right = int(right)

        self.op_type = OperationType(middle)

    def calculate(self, old: int) -> int:
        return calculate(self.left, self.right, self.op_type, old)

@dataclass
class Monkey:
    index: int
    items: List[int]
    op: Operation
    test: Test
    if_true: int # monkey index
    if_false: int # monkey index

    def __init__(self, raw: str):
        monkey, starting, operation, test, iftrue, iffalse = raw.strip().splitlines()
        self.index = int(monkey.split(' ')[1].split(':')[0])
        self.items = [int(worry) for worry in starting.split(': ')[1].split(', ')]
        self.op = Operation(operation.split(': ')[1])
        self.test = Test(test.split(': ')[1])
        self.if_true = int(iftrue.split(' ')[-1])
        self.if_false = int(iffalse.split(' ')[-1])

    def popitem(self) -> int:
        item, self.items = self.items[0], self.items[1:]
        return item

@dataclass
class Input:
    monkeys: List[Monkey]

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        monkeys=[
            Monkey(block) for block in raw.split('\n\n')
        ]
    )

def part1(input: Input) -> Output:
    monkeys = input.monkeys
    gcd = reduce(lambda a,b: a*b, (monkey.test.divisible_by for monkey in monkeys), 1)
    inspections = {m.index: 0 for m in monkeys}

    def throw(worry: int, to_index: int):
        monkeys[to_index].items += [worry % gcd]

    def inspect(monkey: Monkey):
        inspections[monkey.index] += 1

        worry1 = monkey.popitem()
        worry2 = monkey.op.calculate(worry1)
        worry3 = int(worry2 / 3)

        if monkey.test.passes(worry3):
            throw(worry3, monkey.if_true)
        else:
            throw(worry3, monkey.if_false)

    for round in range(1,21):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                inspect(monkey)

    x,y = sorted(inspections.values())[-2:]
    return x*y

def part2(input: Input) -> Output:
    monkeys = input.monkeys
    gcd = reduce(lambda a,b: a*b, (monkey.test.divisible_by for monkey in monkeys), 1)
    inspections = {m.index: 0 for m in monkeys}

    print('gcd', gcd, list(monkey.test.divisible_by for monkey in monkeys))

    def throw(worry: int, to_index: int):
        monkeys[to_index].items += [worry]

    def inspect(monkey: Monkey):
        inspections[monkey.index] += 1

        worry1 = monkey.popitem()
        worry2 = monkey.op.calculate(worry1)
        worry3 = worry2 % gcd

        if monkey.test.passes(worry3):
            throw(worry3, monkey.if_true)
        else:
            throw(worry3, monkey.if_false)

    for round in range(1,10001):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                inspect(monkey)

    x,y = sorted(inspections.values())[-2:]
    return x*y

def main(input_file):
    with open(input_file) as f:
        content = f.read().strip()
        input1 = parse_input(content)
        input2 = parse_input(content)

    print('Part 1:', part1(input1))
    print('Part 2:', part2(input2))

if __name__ == '__main__':
    main(sys.argv[1])
