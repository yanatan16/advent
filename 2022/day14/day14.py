# Advent of Code 2022 Day 14
import sys
from typing import *
from dataclasses import dataclass
import enum

Vertex = Tuple[int,int]
RockPath = List[Vertex]

@dataclass
class Input:
    rocks: List[RockPath]

Output = int

def parse_input(raw: str) -> Input:
    def parse_vertex(s: str) -> Vertex:
        x,y = s.split(',')
        return (int(x), int(y))

    def parse_rock_path(line: str) -> RockPath:
        return [parse_vertex(s) for s in line.split(' -> ')]

    return Input(
        rocks=[
            parse_rock_path(line) for line in raw.splitlines()
        ]
    )

class Value(enum.Enum):
    empty = '.'
    source = '+'
    rock = '#'
    sand = 'o'
    abyss = 'a'

class RockMap:
    map: List[List[Value]]
    def __init__(self, input: Input):
        self.minx = min(x for rockpath in input.rocks for x,_ in rockpath)
        self.maxx = max(x for rockpath in input.rocks for x,_ in rockpath)
        self.miny = min([0] + [y for rockpath in input.rocks for x,y in rockpath])
        self.maxy = max(y for rockpath in input.rocks for x,y in rockpath)

        self.map = [
            [Value.empty for _ in range(0, self.maxx - self.minx + 1)]
            for _ in range(0, self.maxy - self.miny + 1)
        ]

        self.source = (500, 0)
        self._draw_rockpaths(input)

    def _draw_rockpaths(self, input: Input):
        self.set(500, 0, Value.source)
        for rockpath in input.rocks:
            for v1, v2 in zip(rockpath, rockpath[1:]):
                self.draw(v1, v2, Value.rock)

    def set(self, x: int, y: int, v: Value):
        self.map[y-self.miny][x-self.minx] = v

    def get(self, x: int, y: int) -> Value:
        if x < self.minx or x > self.maxx or y < self.miny or y > self.maxy:
            return Value.abyss
        return self.map[y-self.miny][x-self.minx]

    def draw(self, v1: Vertex, v2: Vertex, v: Value):
        if v1[0] != v2[0]:
            x1, x2 = v1[0], v2[0]
            y = v1[1]

            for x in range(min([x1,x2]), max([x1,x2]) + 1):
                self.set(x, y, v)
        else:
            y1, y2 = v1[1], v2[1]
            x = v1[0]

            for y in range(min([y1,y2]), max([y1,y2]) + 1):
                self.set(x, y, v)

    def __str__(self):
        return f'X boundaries: {self.minx} to {self.maxx}\n' +\
          f'Y boundaries: {self.miny} to {self.maxy}\n' +\
          '\n'.join(''.join(v.value for v in row) for row in self.map)

    def drop_sand(self) -> bool:
        x,y = self.source

        if self.get(x, y) == Value.sand:
            return True

        while True:
            down = self.get(x, y+1)
            downleft = self.get(x-1, y+1)
            downright = self.get(x+1, y+1)

            if down == Value.empty:
                y += 1
                continue
            elif down in {Value.sand, Value.rock}:
                if downleft == Value.empty:
                    x = x - 1
                    y = y + 1
                    continue
                elif downleft in {Value.sand, Value.rock}:
                    if downright == Value.empty:
                        x = x + 1
                        y = y + 1
                        continue
                    elif downright in {Value.sand, Value.rock}:
                        self.set(x, y, Value.sand)
                        return False
                    else: #abyss
                        return True
                else: # abyss
                    return True
            else: # abyss
                return True

def part1(input: Input) -> Output:
    map = RockMap(input)

    c = 0
    while not map.drop_sand():
        c += 1
        #print(map)

    return c

class RockMap2(RockMap):
    def __init__(self, input: Input):
        RockMap.__init__(self, input)
        self.maxy += 2
        assert self.miny == 0
        self.minx = min([self.minx, 500 - self.maxy - 2])
        self.maxx = max([self.maxx, 500 + self.maxy + 2])

        self.map = [
            [Value.empty for _ in range(0, self.maxx - self.minx + 1)]
            for _ in range(0, self.maxy - self.miny + 1)
        ]

        self._draw_rockpaths(input)
        self.draw((self.minx, self.maxy), (self.maxx, self.maxy), Value.rock)


def part2(input: Input) -> Output:
    map = RockMap2(input)

    c = 0
    while not map.drop_sand():
        c += 1
        #print(map)

    return c

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
