# Advent of Code 2022 Day 15
import sys
from typing import *
from dataclasses import dataclass
import enum
from functools import cached_property
import tqdm

class Location(NamedTuple):
    x: int
    y: int

    def manhatten_distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    @property
    def tuning_frequency(self) -> int:
        return self.x * 4000000 + self.y

@dataclass
class Signal:
    sensor: Location #13,2
    beacon: Location #15,3

    @cached_property
    def distance(self): #3
        return self.sensor.manhatten_distance(self.beacon)

    def is_covered(self, loc: Location) -> bool:
        return self.distance >= self.sensor.manhatten_distance(loc)

    def next_y_uncovered(self, loc: Location) -> Location:
        #loc: 14,1
        d = self.sensor.manhatten_distance(loc) #2
        xdiff_abs = abs(self.sensor.x - loc.x) #1
        ydiff = loc.y - self.sensor.y #1
        ytarget = self.distance - xdiff_abs #9-6=3

        return Location(x=loc.x, y=loc.y + ytarget - ydiff + 1)

    def covered_x(self) -> Tuple[int, int]:
        return (self.sensor.x - self.distance, self.sensor.x + self.distance)

@dataclass
class Input:
    signals: List[Signal]
    y: int

Output = int

def parse_signal(line: str) -> Signal:
    _, _, sx, sy, _, _, _, _, bx, by = line.split(' ')
    return Signal(
        sensor=Location(x=int(sx[2:-1]), y=int(sy[2:-1])),
        beacon=Location(x=int(bx[2:-1]), y=int(by[2:]))
    )

def parse_input(raw: str, filename: str) -> Input:
    return Input(
        signals=[
            parse_signal(line) for line in raw.splitlines()
        ],
        y=10 if filename == 'example' else 2000000
    )

def part1(input: Input) -> Output:
    return -1

    minx = min([x for s in input.signals for x in s.covered_x()])
    maxx = max([x for s in input.signals for x in s.covered_x()])

    covered = 0
    for x in tqdm.tqdm(range(minx, maxx+1)):
        for signal in input.signals:
            if signal.is_covered(Location(x=x, y=input.y)):
                covered += 1
                break

    taken_spots: Set[Location] = {loc for s in input.signals for loc in [s.sensor, s.beacon]
                                  if loc.y == input.y}

    return covered - len(taken_spots)

def part2(input: Input) -> Output:
    max_xy = input.y * 2

    for x in tqdm.tqdm(range(0, max_xy+1)):
        loc = Location(x=x, y=0)
        while loc.y <= max_xy:
            covered = False
            for i, signal in enumerate(input.signals):
                if signal.is_covered(loc):
                    loc = signal.next_y_uncovered(loc)
                    # print(f'sensor {i} moved location to {loc}')  
                    covered = True
                    break

            if not covered:
                return loc.tuning_frequency

    return -1

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip(), input_file)

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
