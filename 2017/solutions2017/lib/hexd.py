from typing import *

Direction = Literal['ne','nw','se','sw', 'n', 's']

class Coord(NamedTuple):
    q: int
    r: int
    s: int

    def ne(self) -> 'Coord':
        return Coord(q=self.q+1, r=self.r-1, s=self.s)
    def sw(self) -> 'Coord':
        return Coord(q=self.q-1, r=self.r+1, s=self.s)
    def se(self) -> 'Coord':
        return Coord(q=self.q+1, r=self.r, s=self.s-1)
    def nw(self) -> 'Coord':
        return Coord(q=self.q-1, r=self.r, s=self.s+1)
    def north(self) -> 'Coord':
        return Coord(q=self.q, r=self.r-1, s=self.s+1)
    def south(self) -> 'Coord':
        return Coord(q=self.q, r=self.r+1, s=self.s-1)

    def dir(self, direction: Direction) -> 'Coord':
        match direction:
            case 'ne':
                return self.ne()
            case 'nw':
                return self.nw()
            case 'n':
                return self.north()
            case 'se':
                return self.se()
            case 'sw':
                return self.sw()
            case 's':
                return self.south()

    def dist(self) -> int:
        return max([abs(self.q), abs(self.r), abs(self.s)])
