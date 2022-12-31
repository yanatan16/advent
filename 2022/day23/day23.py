# Advent of Code 2022 Day 23
import sys
from typing import *
from dataclasses import dataclass
import enum
from functools import reduce

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

class Location(NamedTuple):
    row: int
    col: int

    def __str__(self):
        return f'({self.row},{self.col})'

class Direction(enum.Enum):
    north = 0
    south = 1
    west = 2
    east = 3

def freqs(ls):
    d = {}
    for item in ls:
        d[item] = d.get(item, 0) + 1
    return d

@dataclass
class State:
    elves: Set[Location]
    iteration: int = 0

    def __init__(self, input: Input):
        self.elves = {
            Location(i,j)
            for i in range(len(input.lines))
            for j in range(len(input.lines[i]))
            if input.lines[i][j] == '#'
        }

    def propose_move(self, elf: Location) -> Location:
        nomove_checks = [Location(elf.row+i, elf.col+j)
                         for i in (-1,0,1)
                         for j in (-1,0,1)
                         if (i != 0 or j != 0)]
        if all(check not in self.elves for check in nomove_checks):
            return elf

        for diri in range(4):
            direction = Direction((diri + self.iteration) % 4)

            if direction == Direction.north:
                checks = [Location(elf.row-1, elf.col+i) for i in (-1,0,1)]
            elif direction == Direction.south:
                checks = [Location(elf.row+1, elf.col+i) for i in (-1,0,1)]
            elif direction == Direction.west:
                checks = [Location(elf.row+i, elf.col-1) for i in (-1,0,1)]
            else: # direction == Direction.east:
                checks = [Location(elf.row+i, elf.col+1) for i in (-1,0,1)]

            if all(check not in self.elves for check in checks):
                return checks[1]

        return elf


    def iterate(self) -> bool:
        # first half
        proposals: List[Tuple[Location, Location]] = [
            (elf, self.propose_move(elf))
            for elf in self.elves
        ]
        proposal_freqs = freqs(prop for _, prop in proposals)

        # second half
        new_elves = {
            proposed if proposal_freqs[proposed] == 1 else current
            for current, proposed in proposals
        }

        nomove = new_elves == self.elves

        self.elves = new_elves
        self.iteration += 1

        return nomove

    @property
    def empty_ground_tiles(self):
        height = max(e.row for e in self.elves) - min(e.row for e in self.elves) + 1
        width = max(e.col for e in self.elves) - min(e.col for e in self.elves) + 1
        return height * width - len(self.elves)

    def __str__(self):
        bottom = max(e.row for e in self.elves)
        top = min(e.row for e in self.elves)
        right = max(e.col for e in self.elves)
        left = min(e.col for e in self.elves)

        return f'Iteration {self.iteration}:\n' + '\n'.join(
            ''.join(
                '#' if Location(i,j) in self.elves else '.'
                for j in range(left, right+1)
            )
            for i in range(top, bottom+1)
        )
import ipdb
def part1(input: Input) -> Output:
    state = State(input)
    # print(state)

    for rnd in range(10):
        # ipdb.set_trace()
        state.iterate()
        # print(state)

    return state.empty_ground_tiles

def part2(input: Input) -> Output:
    state = State(input)
    end = False
    
    while not end:
        end = state.iterate()

    return state.iteration

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
