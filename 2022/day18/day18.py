# Advent of Code 2022 Day 18
import sys
from typing import *
from dataclasses import dataclass
import enum
from collections import namedtuple

class Cube(NamedTuple):
    x:int
    y:int
    z:int

    @property
    def adjacent_cubes(self) -> List['Cube']:
        return [
            Cube(x=self.x-1,y=self.y,z=self.z),
            Cube(x=self.x+1,y=self.y,z=self.z),
            Cube(x=self.x,y=self.y-1,z=self.z),
            Cube(x=self.x,y=self.y+1,z=self.z),
            Cube(x=self.x,y=self.y,z=self.z-1),
            Cube(x=self.x,y=self.y,z=self.z+1),
        ]

    @property
    def lines(self) -> List['Cube']:
        return [
            Cube(x=self.x,y=self.y,z=-1),
            Cube(x=self.x,y=-1,z=self.z),
            Cube(x=-1,y=self.y,z=self.z)
        ]

def parse_cube(line:str) -> Cube:
    x,y,z = line.split(',')
    return Cube(x=int(x),y=int(y),z=int(z))

@dataclass
class Input:
    cubes: List[Cube]

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        cubes=[
            parse_cube(line) for line in raw.splitlines()
        ]
    )

def part1(input: Input) -> Output:
    surface_area = len(input.cubes) * 6
    cubeset = set(input.cubes)

    for cube in input.cubes:
        surface_area -= sum(1 if adj in cubeset else 0 for adj in cube.adjacent_cubes)

    return surface_area

def part2(input: Input) -> Output:
    cubeset = set(input.cubes)
    surface_area = part1(input)

    minx, maxx = min(c.x for c in input.cubes), max(c.x for c in input.cubes)
    miny, maxy = min(c.y for c in input.cubes), max(c.y for c in input.cubes)
    minz, maxz = min(c.z for c in input.cubes), max(c.z for c in input.cubes)

    grid = [[['#' if Cube(x,y,z) in cubeset else '.' for x in range(minx-1, maxx+2)]
             for y in range(miny-1, maxy+2)]
            for z in range(minz-1, maxz + 2)]

    def getg(c):
        try:
            return grid[c.z][c.y][c.x]
        except:
            print('Failed to find', c)
            raise
    def setg(c, v):
        grid[c.z][c.y][c.x] = v

    def walk(c: Cube) -> Tuple[List[Cube], int]:
        if getg(c) == '.':
            setg(c, 'v')

            adjcubes = [c for c in c.adjacent_cubes
                        if minx-1 <= c.x <= maxx+1
                        and miny-1 <= c.y <= maxy+1
                        and minz-1 <= c.z <= maxz+1]
            return [c for c in adjcubes if getg(c) == '.']
        elif getg(c) == '#':
            return []
        elif getg(c) == 'v':
            return []

    nodes = [Cube(minx-1,miny-1,minz-1)]
    while len(nodes):
        node, nodes = nodes[0], nodes[1:]
        nodes += walk(node)

    empty = [Cube(x,y,z)
              for x in range(minx-1,maxx+2)
              for y in range(miny-1,maxy+2)
              for z in range(minz-1,maxz+2)
              if getg(Cube(x,y,z)) == '.'
            ]

    return part1(input) - part1(Input(cubes=empty))

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
