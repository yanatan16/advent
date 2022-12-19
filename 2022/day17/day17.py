# Advent of Code 2022 Day 17
import sys
from typing import *
from dataclasses import dataclass
import enum

Row = List[bool] # length 7
Rock = List[Row]
Tower = List[Row] # length 7
initial_tower = [[True,True,True,True,True,True,True]]

rocks: List[Rock] = [
    [[False, False, True, True, True, True, False]],
    [[False, False, False, True, False, False, False],
     [False, False, True, True, True, False, False],
     [False, False, False, True, False, False, False],
     ],
    [[False, False, False, False, True, False, False],
     [False, False, False, False, True, False, False],
     [False, False, True, True, True, False, False],
     ],
    [[False,False,True,False,False,False,False] for _ in range(4)],
    [[False,False,True,True,False,False,False] for _ in range(2)],
]

@dataclass
class Input:
    arrows: str

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        arrows = raw.splitlines()[0]
    )

def shift_rock(rock, left=False):
    if left:
        if any(line[0] for line in rock):
            return rock
        else:
            return [line[1:]+[False] for line in rock]
    else:
        if any(line[-1] for line in rock):
            return rock
        else:
            return [[False] + line[:-1] for line in rock]

def intersects_tower(rock, tower, rock_level):
    for i, row in enumerate(rock[::-1]):
        level = rock_level + i
        if level >= len(tower):
            pass
        else:
            for j, column in enumerate(row):
                if column and tower[level][j]:
                    return True
    return False

def try_shift_rock(rock, tower, rock_level, left=False):
    next_rock = shift_rock(rock, left)
    if intersects_tower(next_rock, tower, rock_level):
        return rock
    else:
        return next_rock

def can_drop_rock(rock, tower, rock_level):
    if intersects_tower(rock, tower, rock_level - 1):
        return False
    else:
        return True

def land_rock(rock, tower, rock_level):
    new_tower = tower
    for i, row in enumerate(rock[::-1]):
        level = rock_level + i
        if len(tower) == level:
            new_tower += [[False for _ in range(7)]]
        new_tower[level] = [row[j] or tower[level][j] for j in range(7)]
    return new_tower

def print_row(row):
    return '|' + ''.join('#' if el else '.' for el in row) + '|'
def print_tower(tower):
    return '\n'.join(str(i) + print_row(row) for i,row in enumerate(tower[::-1]))


@dataclass
class State1:
    tower: Tower
    next_rock: int
    arrows: str
    next_arrow: int

    def __str__(self):
        return print_tower(self.tower)

    def simulate_next_rock(self) -> 'State1':
        rock = rocks[self.next_rock]

        ## do stuff
        rock_level = len(self.tower) + 3
        next_arrow = self.next_arrow

        while True:
            # try moving with arrow
            arrow = self.arrows[next_arrow]
            rock = try_shift_rock(rock, self.tower, rock_level,
                                  left=True if arrow == '<' else False)
            next_arrow = (next_arrow + 1) % len(self.arrows)

            # try_dropping
            if can_drop_rock(rock, self.tower, rock_level):
                rock_level -= 1
            else:
                new_tower = land_rock(rock, self.tower, rock_level)
                break

        return State1(tower=new_tower,
                      next_rock=(self.next_rock + 1) % len(rocks),
                      arrows=self.arrows,
                      next_arrow=next_arrow)

def search_for_patterns(tower):
    n = 2623
    pattern = tower[-n:]
    print('Searching for pattern')
    print(print_tower(pattern))
    last = 0

    for i in range(len(tower)):
        if tower[i:(i+n)] == pattern:
            print(f'Found pattern at {i} (diff: {i-last})')
            last = i


def part1(input: Input) -> Output:
    state = State1(tower=[row for row in initial_tower], next_rock=0, arrows=input.arrows, next_arrow=0)
    times = 2022
    for i in range(times):
        state = state.simulate_next_rock()

    #print(state)
    #search_for_patterns(state.tower)

    return len(state.tower) - 1



def part2(input: Input) -> Output:
    state = State1(tower=initial_tower, next_rock=0, arrows=input.arrows, next_arrow=0)
    times = 200 + 1700 * 10

    base_height = 318
    base_rocks = 200
    cycle_height = 2623
    cycle_rocks = 1700

    target = 1000000000000
    
    for i in range(times):
        if i <= 200:
            print(i, len(state.tower) - 1)
        if (i - 200) % 1700 == 0:
            height = len(state.tower) - 1
            guess = base_height + cycle_height * int((i - base_rocks) / cycle_rocks)
            if guess != height:
                print(f'i {i} guess wrong! height {height} guess {guess}')
                return -1

        state = state.simulate_next_rock()

    #print(print_tower(state.tower))
    #search_for_patterns(state.tower)

    cycles = int((target - base_rocks) / cycle_rocks)

    return base_height + cycles * cycle_height

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
