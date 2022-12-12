# Advent of Code 2022 Day 12
import sys
from typing import *
from dataclasses import dataclass
import enum

Grid = List[List[str]]
Position = Tuple[int,int]

@dataclass
class Input:
    start: Position
    end: Position
    grid: Grid

Output = int

def parse_input(raw: str) -> Input:
    grid = [line for line in raw.splitlines()]
    start = [(i,j) for i in range(len(grid)) for j in range(len(grid[0]))
             if grid[i][j] == 'S'][0]
    end = [(i,j) for i in range(len(grid)) for j in range(len(grid[0]))
             if grid[i][j] == 'E'][0]

    return Input(
        start=start,
        end=end,
        grid=grid
    )

def in_grid(grid: Grid, pos: Position) -> bool:
    x,y = pos
    return not (x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]))

def height(grid: Grid, pos: Position) -> int:
    x,y = pos
    h = grid[x][y]
    if h == 'S':
        return ord('a')
    elif h == 'E':
        return ord('z')
    else:
        return ord(h)

def destinations(grid: Grid, cur: Position) -> [Position]:
    x,y = cur
    cur_height = height(grid, cur)
    dests = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
    return [
        d for d in dests
        if in_grid(grid, d)
        and height(grid, d) - cur_height <= 1
    ]

def shortest_path(input: Input, override_start: Optional[Position] = None) -> int:
    grid = input.grid
    distances: Dict[Position, int] = {}
    neighbors: Dict[Position, int] = {override_start if override_start else input.start: 0}

    while input.end not in distances:
        if len(neighbors) == 0:
            return 10000000

        dist, cur_pos = min((v,k) for k,v in neighbors.items())
        del neighbors[cur_pos]
        distances[cur_pos] = dist

        for dest in destinations(grid, cur_pos):
            if override_start is not None and height(grid, dest) == ord('a'):
                continue
            elif dest in distances and distances.get(dest) <= dist+1:
                continue
            else:
                neighbors[dest] = min([
                    dist + 1,
                    neighbors.get(dest, dist+1)
                ])

    return distances[input.end]

def part1(input: Input) -> Output:
    return shortest_path(input)

def part2(input: Input) -> Output:
    all_as = [(i,j)
              for i in range(len(input.grid))
              for j in range(len(input.grid[0]))
              if height(input.grid, (i,j)) == ord('a')]
    return min(shortest_path(input, override_start=pos) for pos in all_as)

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
