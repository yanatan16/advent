# Advent of Code 2022 Day 22
import sys
from typing import *
from dataclasses import dataclass
import enum
from functools import reduce

class Tile(enum.Enum):
    empty = ' '
    open = '.'
    wall = '#'

@dataclass
class Instruction:
    distance: Optional[int]
    turn: Optional[str]

    def __str__(self):
        if self.distance is not None:
            return str(self.distance)
        else:
            return self.turn


def parse_instructions(raw: str) -> List[Instruction]:
    instrs = []
    while len(raw) > 0:
        if raw[0] in '0123456789':
            next_num = ''
            while len(raw) > 0 and raw[0] in '0123456789':
                next_num += raw[0]
                raw = raw[1:]

            instrs += [Instruction(distance=int(next_num), turn=None)]

        else:
            instrs += [Instruction(distance=None, turn=raw[0])]
            raw = raw[1:]

    return instrs

@dataclass
class Input:
    board: List[List[Tile]]
    instructions: List[Instruction]

Output = int

def parse_input(raw: str) -> Input:
    board, instructions = raw.split('\n\n')

    return Input(
        board=[
            [Tile(tile) for tile in line] for line in board.splitlines()
        ],
        instructions=parse_instructions(instructions)
    )

class Location(NamedTuple):
    row: int
    col: int

@dataclass
class Board:
    board: List[List[Tile]]

    def lookup(self, loc: Location) -> Tile:
        if loc.row < 1 or loc.col < 1:
            return Tile.empty
        elif loc.row > len(self.board) or loc.col > len(self.board[loc.row-1]):
            return Tile.empty

        return self.board[loc.row-1][loc.col-1]

    def find_wrap(self, row=None, col=None, first=False, last=False) -> Location:
        if row is not None:
            if first:
                for col in range(1, len(self.board[row-1])+1):
                    if self.lookup(Location(row, col)) != Tile.empty:
                        return Location(row, col)
            else:
                for col in range(len(self.board[row-1]), 0, -1):
                    if self.lookup(Location(row, col)) != Tile.empty:
                        return Location(row, col)
        else: # col is not None
            if first:
                for row in range(1, len(self.board)+1):
                    if self.lookup(Location(row, col)) != Tile.empty:
                        return Location(row, col)
            else:
                for row in range(len(self.board), 0, -1):
                    if self.lookup(Location(row, col)) != Tile.empty:
                        return Location(row, col)

class Facing(enum.Enum):
    right = 0
    down = 1
    left = 2
    up = 3

    def turn(self, direction: str) -> 'Facing':
        if direction == 'R':
            return Facing((self.value + 1) % 4)
        else:
            return Facing((self.value - 1) % 4)

    def next_loc(self, board: Board, loc: Location) -> Location:
        if self == Facing.right:
            nloc = Location(loc.row, loc.col + 1)
        elif self == Facing.left:
            nloc = Location(loc.row, loc.col - 1)
        elif self == Facing.up:
            nloc = Location(loc.row - 1, loc.col)
        else:
            nloc = Location(loc.row + 1, loc.col)

        if board.lookup(nloc) != Tile.empty:
            return nloc

        if self == Facing.right:
            return board.find_wrap(row=nloc.row, first=True)
        elif self == Facing.left:
            return board.find_wrap(row=nloc.row, last=True)
        elif self == Facing.up:
            return board.find_wrap(col=nloc.col, last=True)
        else:
            return board.find_wrap(col=nloc.col, first=True)



def part1(input: Input) -> Output:
    board = Board(input.board)

    start = board.find_wrap(row=1, first=True)
    current = start
    facing = Facing.right

    # import ipdb; ipdb.set_trace()
    # print(f'start: now at {current} facing {facing}')

    for instruction in input.instructions:
        if instruction.distance is not None:
            for i in range(instruction.distance):
                next_tile = facing.next_loc(board, current)
                if board.lookup(next_tile) == Tile.wall:
                    break
                else:
                    current = next_tile
        else:
            facing = facing.turn(instruction.turn)

        # print(f'after instr ({instruction}): now at {current} facing {facing}')

    return 1000 * current.row + 4 * current.col + facing.value

@dataclass
class CubeLocation:
    face: int
    row: int
    col: int

def transpose(matrix):
    return [[matrix[i][j] for i in range(len(matrix[j]))] for j in range(len(matrix))]

def reverse(matrix):
    return [row[::-1] for row in matrix]

@dataclass
class Cube:
    length: int
    faces: List[List[List[Tile]]]

    def __init__(self, board: List[List[Tile]]):
        if len(board) == 12:
            length = 4
        elif len(board) == 16:
            length = 4
        else:
            length = 50
        self.length = length

        if len(board) == 12:
            self.faces = [
                [[board[i][j+2*length] for j in range(length)] for i in range(length)],
                [[board[i+length][j] for j in range(length)] for i in range(length)],
                [[board[i+length][j+length] for j in range(length)] for i in range(length)],
                [[board[i+length][j+2*length] for j in range(length)] for i in range(length)],
                [[board[i+2*length][j+2*length] for j in range(length)] for i in range(length)],
                [[board[i+2*length][j+3*length] for j in range(length)] for i in range(length)],
            ]
        else:
            self.faces = [
                [[board[i+0*length][j+1*length] for j in range(length)] for i in range(length)],
                reverse(transpose(
                    [[board[i+3*length][j+0*length] for j in range(length)] for i in range(length)]
                )),
                reverse(transpose(
                    [[board[i+2*length][j+0*length] for j in range(length)] for i in range(length)]
                )),
                [[board[i+1*length][j+1*length] for j in range(length)] for i in range(length)],
                [[board[i+2*length][j+1*length] for j in range(length)] for i in range(length)],
                reverse(
                    [[board[i+0*length][j+2*length] for j in range(length)] for i in range(length)]
                )[::-1],
            ]


    #   1
    # 234
    #   56

    #  16
    #  4
    # 35
    # 2

    #     11116666
    #     11116666
    #     11116666
    #     11116666
    #     4444
    #     4444
    #     4444
    #     4444
    # 33335555
    # 33335555
    # 33335555
    # 33335555
    # 2222
    # 2222
    # 2222
    # 2222

    def to_map_location(self, loc: CubeLocation) -> Location:
        if self.length == 4:
            if loc.face == 1:
                return Location(loc.row + 0*self.length, loc.col + 2*self.length)
            elif loc.face == 2:
                return Location(loc.row + 1*self.length, loc.col + 0*self.length)
            elif loc.face == 3:
                return Location(loc.row + 1*self.length, loc.col + 1*self.length)
            elif loc.face == 4:
                return Location(loc.row + 1*self.length, loc.col + 2*self.length)
            elif loc.face == 5:
                return Location(loc.row + 2*self.length, loc.col + 2*self.length)
            elif loc.face == 6:
                return Location(loc.row + 2*self.length, loc.col + 3*self.length)
        else:
            if loc.face == 1:
                return Location(loc.row + 0*self.length, loc.col + 1*self.length)
            elif loc.face == 2:
                loc = CubeLocation(loc.face, loc.col, self.length - loc.row + 1)
                return Location(loc.row + 3*self.length, loc.col + 0*self.length)
            elif loc.face == 3:
                loc = CubeLocation(loc.face, loc.col, self.length - loc.row + 1)
                return Location(loc.row + 2*self.length, loc.col + 0*self.length)
            elif loc.face == 4:
                return Location(loc.row + 1*self.length, loc.col + 1*self.length)
            elif loc.face == 5:
                return Location(loc.row + 2*self.length, loc.col + 1*self.length)
            elif loc.face == 6:
                loc = CubeLocation(loc.face, loc.row, self.length - loc.col + 1)
                return Location(loc.row + 0*self.length, loc.col + 2*self.length)



    def lookup(self, loc: CubeLocation) -> Tile:
        return self.faces[loc.face-1][loc.row-1][loc.col-1]

    def walk(self, loc: CubeLocation, facing: Facing) -> (CubeLocation, Facing):
        def inv(n):
            return self.length - n + 1

        if facing == Facing.right:
            if loc.col == self.length:
                if loc.face == 1:
                    return CubeLocation(6, inv(loc.row), self.length), Facing.left
                elif loc.face == 2:
                    return CubeLocation(3, loc.row, 1), Facing.right
                elif loc.face == 3:
                    return CubeLocation(4, loc.row, 1), Facing.right
                elif loc.face == 4:
                    return CubeLocation(6, 1, inv(loc.row)), Facing.down
                elif loc.face == 5:
                    return CubeLocation(6, loc.row, 1), Facing.right
                elif loc.face == 6:
                    return CubeLocation(1, inv(loc.row), self.length), Facing.left


            return CubeLocation(loc.face, loc.row, loc.col + 1), facing
        elif facing == Facing.left:
            if loc.col == 1:
                if loc.face == 1:
                    return CubeLocation(3, 1, loc.row), Facing.down
                elif loc.face == 2:
                    return CubeLocation(6, self.length, inv(loc.row)), Facing.up
                elif loc.face == 3:
                    return CubeLocation(2, loc.row, self.length), Facing.left
                elif loc.face == 4:
                    return CubeLocation(3, loc.row, self.length), Facing.left
                elif loc.face == 5:
                    return CubeLocation(5, self.length, inv(loc.row)), Facing.up
                elif loc.face == 6:
                    return CubeLocation(5, loc.row, self.length), Facing.left

            return CubeLocation(loc.face, loc.row, loc.col - 1), Facing.left
        elif facing == Facing.up:
            if loc.row == 1:
                if loc.face == 1:
                    return CubeLocation(2, 1, inv(loc.col)), Facing.down
                elif loc.face == 2:
                    return CubeLocation(1, 1, inv(loc.col)), Facing.down
                elif loc.face == 3:
                    return CubeLocation(1, loc.col, 1), Facing.right
                elif loc.face == 4:
                    return CubeLocation(1, self.length, loc.col), Facing.up
                elif loc.face == 5:
                    return CubeLocation(4, self.length, loc.col), Facing.up
                elif loc.face == 6:
                    return CubeLocation(4, inv(loc.col), self.length), Facing.left

            return CubeLocation(loc.face, loc.row - 1, loc.col), Facing.up
        else: # Facing.down
            if loc.row == self.length:
                if loc.face == 1:
                    return CubeLocation(4, 1, loc.col), Facing.down
                elif loc.face == 2:
                    return CubeLocation(5, self.length, inv(loc.col)), Facing.up
                elif loc.face == 3:
                    return CubeLocation(5, inv(loc.col), 1), Facing.right
                elif loc.face == 4:
                    return CubeLocation(5, 1, loc.col), Facing.down
                elif loc.face == 5:
                    return CubeLocation(2, self.length, inv(loc.col)), Facing.up
                elif loc.face == 6:
                    return CubeLocation(2, inv(loc.col), 1), Facing.right

            return CubeLocation(loc.face, loc.row + 1, loc.col), Facing.down


@dataclass
class InputCube:
    length: int
    faces: List[List[List[Tile]]]

    face_locations = [
        (0,1),
        (0,2),
        (1,1),
        (2,0),
        (2,1),
        (3,0)
    ]

    face_edges = [
        {
            Facing.down: (3, Facing.down, False),
            Facing.right: (2, Facing.right, False),
            Facing.up: (6, Facing.right, False),
            Facing.left: (4, Facing.right, True)
        },
        {
            Facing.up: (6, Facing.up, False), #??
            Facing.down: (3, Facing.left, False),
            Facing.left: (1, Facing.left, False),
            Facing.right: (5, Facing.left, True),
        },
        {
            Facing.up: (1, Facing.up, False),
            Facing.down: (5, Facing.down, False),
            Facing.left: (4, Facing.down, False),
            Facing.right: (2, Facing.up, False),
        },
        {
            Facing.up: (3, Facing.right, False),
            Facing.down: (6, Facing.down, False),
            Facing.left: (1, Facing.right, True),
            Facing.right: (5, Facing.right, False),
        },
        {
            Facing.up: (3, Facing.up, False),
            Facing.down: (6, Facing.left, False),
            Facing.left: (4, Facing.left, False),
            Facing.right: (2, Facing.left, True),
        },
        {
            Facing.up: (4, Facing.up, False),
            Facing.down: (2, Facing.down, False), #??
            Facing.left: (1, Facing.down, False),
            Facing.right: (5, Facing.up, False),
        },
    ]

    #     11112222
    #     11112222
    #     11112222
    #     11112222
    #     3333
    #     3333
    #     3333
    #     3333
    # 44445555
    # 44445555
    # 44445555
    # 44445555
    # 6666
    # 6666
    # 6666
    # 6666


    def __init__(self, board: List[List[Tile]]):
        if len(board) == 16:
            length = 4
        else:
            length = 50

        self.length = length

        self.faces = [
            [[board[i+yoffset*length][j+xoffset*length] for j in range(length)]
             for i in range(length)]
            for (yoffset, xoffset) in self.face_locations
        ]

    def to_map_location(self, loc: CubeLocation) -> Location:
        yoffset, xoffset = self.face_locations[loc.face-1]
        return Location(loc.row + yoffset * self.length, loc.col + xoffset * self.length)

    def lookup(self, loc: CubeLocation) -> Tile:
        return self.faces[loc.face-1][loc.row-1][loc.col-1]

    def walk(self, loc: CubeLocation, facing: Facing) -> (CubeLocation, Facing):
        if (facing == Facing.right and loc.col == self.length) or\
           (facing == Facing.left and loc.col == 1) or\
           (facing == Facing.up and loc.row == 1) or\
           (facing == Facing.down and loc.row == self.length):

            edge = self.face_edges[loc.face-1][facing]
            to_face, to_facing, inverted = edge

            if facing in {Facing.left, Facing.right}:
                free_var = loc.row
            else:
                free_var = loc.col

            if inverted:
                free_var = self.length - free_var + 1

            if to_facing == Facing.left:
                return CubeLocation(to_face, free_var, self.length), to_facing
            elif to_facing == Facing.right:
                return CubeLocation(to_face, free_var, 1), to_facing
            elif to_facing == Facing.up:
                return CubeLocation(to_face, self.length, free_var), to_facing
            elif to_facing == Facing.down:
                return CubeLocation(to_face, 1, free_var), to_facing

        else:
            return CubeLocation(
                loc.face,
                loc.row + (1 if facing == Facing.down else 0) + (-1 if facing == Facing.up else 0),
                loc.col + (1 if facing == Facing.right else 0) + (-1 if facing == Facing.left else 0),
            ), facing

def part2(input: Input) -> Output:
    if len(input.board) == 12:
        cube = Cube(input.board)
    else:
        cube = InputCube(input.board)

    for face in range(1,7):
        print(f'face {face}:')
        print('\n'.join(''.join(t.value for t in row) for row in cube.faces[face-1]))

    start = CubeLocation(1,1,1)
    current = start
    facing = Facing.right

    print(f'start: now at {current} facing {facing}')
    print(f'executing {len(input.instructions)} instructions')

    for instri, instruction in enumerate(input.instructions):
        start_face = current.face
        start_facing = facing
        if instruction.distance is not None:
            for i in range(instruction.distance):
                next_tile, next_facing = cube.walk(current, facing)
                if cube.lookup(next_tile) == Tile.wall:
                    break
                else:
                    current = next_tile
                    facing = next_facing

        else:
            facing = facing.turn(instruction.turn)

        print(f'after instr {instri} ({instruction}): now at {current} facing {facing}')
        # if current.face != start_face and facing != start_facing:
            # import ipdb; ipdb.set_trace()

    maploc = cube.to_map_location(current)
    print(f'convert {current} to {maploc}')
    return 1000 * maploc.row + 4 * maploc.col + facing.value

def main(input_file, skip=None):
    with open(input_file) as f:
        input = parse_input(f.read().rstrip())

    if skip != 'skip':
        print('Part 1:', part1(input))
    else:
        print('Skipping Part 1')
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(*sys.argv[1:])
