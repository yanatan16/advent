# Advent of Code 2022 Day 24
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

class Direction(enum.Enum):
    up = '^'
    down = 'v'
    left = '<'
    right = '>'

class Location(NamedTuple):
    row: int
    col: int

    @property
    def up(self) -> 'Location':
        return Location(self.row-1,self.col)
    @property
    def down(self) -> 'Location':
        return Location(self.row+1,self.col)
    @property
    def left(self) -> 'Location':
        return Location(self.row,self.col-1)
    @property
    def right(self) -> 'Location':
        return Location(self.row,self.col+1)

@dataclass
class Map:
    width: int
    height: int
    start_col: int
    end_col: int

    def __init__(self, input: Input):
        self.height = len(input.lines) - 2
        self.width = len(input.lines[0]) - 2
        self.start_col = [i for i in range(self.width+2) if input.lines[0][i] == '.'][0]
        self.end_col = [i for i in range(self.width+2) if input.lines[self.height+1][i] == '.'][0]

    def in_map(self, loc: Location) -> bool:
        if loc.row == 0:
            return loc.col == self.start_col
        elif loc.row == self.height + 1:
            return loc.col == self.end_col
        else:
            return 1 <= loc.row <= self.height and 1 <= loc.col <= self.width

    def is_at_end(self, loc: Location) -> bool:
        return loc.row == self.height + 1 and loc.col == self.end_col


class Blizzard(NamedTuple):
    loc: Location
    dir: Direction

    def next(self, map: Map) -> 'Blizzard':
        if self.dir == Direction.down:
            if self.loc.row == map.height:
                return Blizzard(Location(1, self.loc.col), self.dir)
            else:
                return Blizzard(Location(self.loc.row + 1, self.loc.col), self.dir)
        elif self.dir == Direction.up:
            if self.loc.row == 1:
                return Blizzard(Location(map.height, self.loc.col), self.dir)
            else:
                return Blizzard(Location(self.loc.row - 1, self.loc.col), self.dir)
        elif self.dir == Direction.right:
            if self.loc.col == map.width:
                return Blizzard(Location(self.loc.row, 1), self.dir)
            else:
                return Blizzard(Location(self.loc.row, self.loc.col + 1), self.dir)
        else: # self.dir == Direction.left:
            if self.loc.col == 1:
                return Blizzard(Location(self.loc.row, map.width), self.dir)
            else:
                return Blizzard(Location(self.loc.row, self.loc.col - 1), self.dir)

@dataclass
class State:
    map: Map
    blizzards: List[Blizzard]
    positions: Set[Location]
    goal_position: Location

    @staticmethod
    def parse(input:Input):
        map = Map(input)
        blizzards = [
            Blizzard(Location(i,j), Direction(input.lines[i][j]))
            for i in range(len(input.lines))
            for j in range(len(input.lines[i]))
            if input.lines[i][j] in '<>^v'
        ]
        positions = {Location(0, map.start_col)}

        return State(map, blizzards, positions, Location(map.height+1,map.end_col))

    def next_state(self) -> 'State':
        next_blizzards = [b.next(self.map) for b in self.blizzards]
        next_blizzard_locations = {b.loc for b in next_blizzards}
        next_positions = {
            p_pos
            for pos in self.positions
            for p_pos in (pos, pos.up, pos.down, pos.left, pos.right)
            if self.map.in_map(p_pos)
            and p_pos not in next_blizzard_locations
        }


        return State(map=self.map,
                     blizzards=next_blizzards,
                     positions=next_positions,
                     goal_position=self.goal_position)

    def solved(self):
        return any(pos == self.goal_position for pos in self.positions)

def part1(input: Input) -> Output:
    state = State.parse(input)
    rnd = 0

    while not state.solved():
        state = state.next_state()
        rnd += 1

    return rnd

def part2(input: Input) -> Output:
    state = State.parse(input)

    start_pos = Location(0, state.map.start_col)
    end_pos = Location(state.map.height+1, state.map.end_col)

    first_rnd = 0
    while not state.solved():
        state = state.next_state()
        first_rnd += 1

    print(f'solved first traverse in {first_rnd}')

    state = State(
        map=state.map,
        blizzards=state.blizzards,
        positions={end_pos},
        goal_position=start_pos
    )

    second_rnd = 0
    while not state.solved():
        state = state.next_state()
        second_rnd += 1

    print(f'solved second traverse in {second_rnd}')

    state = State(
        map=state.map,
        blizzards=state.blizzards,
        positions={start_pos},
        goal_position=end_pos
    )

    third_rnd = 0
    while not state.solved():
        state = state.next_state()
        third_rnd += 1

    print(f'solved third traverse in {third_rnd}')

    return first_rnd + second_rnd + third_rnd

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
