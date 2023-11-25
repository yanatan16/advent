
from typing import *
from solutions2017.lib import Advent

Input = int

class Day3(Advent[Input]):
    day = 3

    samples = ['1024']

    layers = [(i, ((i-1)*2+1)**2, (i*2+1)**2) for i in range(10000)]

    def layer(self, x: int) -> int:
        if x == 1:
            return 0
        for i, low, high in self.layers:
            if low < x <= high:
                return i

    def position(self, x: int) -> Tuple[int, int]:
        layer = self.layer(x)
        r, low, high = self.layers[layer]
        total = high - low
        height = r * 2 + 1

        diff = x - low

        if diff <= (height-1):
            return (r, -r + diff)
        elif (height-1) < diff <= 2*(height-1):
            return (r - (diff - (height-1)), r)
        elif 2*(height-1) < diff <= 3*(height-1):
            return (-r, r - (diff - (2*(height-1))))
        else:
            return (-r + (diff - (3*(height-1))), -r)

    def parse(self, raw: str) -> Input:
        return int(raw.strip())

    def solve1(self, input: Input) -> Any:
        x, y = self.position(input)
        return abs(x) + abs(y)

    def solve2(self, input: Input) -> Any:
        size = 50
        squares = [[None for _ in range(size)] for _ in range(size)]

        center = int(size / 2)
        squares[center][center] = 1

        for i in range(size**2):
            if i == 0:
                continue

            x,y = self.position(i + 1)
            ix = center + x
            iy = center + y

            square = [line[(iy-1):(iy+2)] for line in squares[(ix-1):(ix+2)]]

            if len(square) < 3 or len(square[0]) < 3:
                print('final squares')
                print(squares)
                raise RuntimeError('Square is not big enough')

            value = sum(square[a][b] for a, b in [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
                        if square[a][b] is not None)

            squares[ix][iy] = value

            if value > input:
                return value

if __name__ == '__main__':
    Day3().main()
