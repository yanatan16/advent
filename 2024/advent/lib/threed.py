from typing import *
import math

T = TypeVar('T')

class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z
        )

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z
        )

    def __mul__(self, other: int) -> 'Coord':
        return Coord(x=self.x*other,y=self.y*other,z=self.z*other)

    def __truediv__(self, other: int) -> 'Coord':
        return Coord(x=self.x/other,y=self.y/other,z=self.z/other)

    def __eq__(self, other: 'Coord') -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z


    def norm1(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def norm2(self) -> float:
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def neighbors(self) -> List['Coord']:
        return [
            Coord(x=self.x+1, y=self.y, z=self.z),
            Coord(x=self.x-1, y=self.y, z=self.z),
            Coord(x=self.x, y=self.y+1, z=self.z),
            Coord(x=self.x, y=self.y-1, z=self.z),
            Coord(x=self.x, y=self.y, z=self.z+1),
            Coord(x=self.x, y=self.y, z=self.z-1),
        ]

    def get(self, map: List[List[List[T]]]) -> T | None:
        assert len(map) > 0, 'Map must have at least one row'
        assert len(map[0]) > 0, 'Map must have at least one column'
        assert len(map[0][0]) > 0, 'Map must have at least one third dimension'

        return (
            map[self.x][self.y][self.z]
            if 0 <= self.x < len(map)
            and 0 <= self.y < len(map[self.x])
            and 0 <= self.z < len(map[self.x][self.y])
            else None
        )

    def __str__(self) -> str:
        return f'({self.x},{self.y},{self.z})'
