from typing import *

T = TypeVar('T')

Direction = Literal['up','down','left','right']

right_turn: Dict[Direction, Direction] = {
    'up': 'right',
    'down': 'left',
    'right': 'down',
    'left': 'up',
}
left_turn = {v:k for k,v in right_turn.items()}

class Coord(NamedTuple):
    x: int
    y: int

    def neighbors(self, diagnols: bool = False) -> List['Coord']:
        return [
            Coord(x=self.x+1, y=self.y),
            Coord(x=self.x-1, y=self.y),
            Coord(x=self.x, y=self.y+1),
            Coord(x=self.x, y=self.y-1)
        ] + (
            [Coord(x=self.x+1,y=self.y+1),
             Coord(x=self.x+1,y=self.y-1),
             Coord(x=self.x-1,y=self.y-1),
             Coord(x=self.x-1,y=self.y+1)]
            if diagnols else []
        )

    def inbounds(self, xmax_or_map: int | List[List[T]], ymax: int = 0, xmin: int = 0, ymin: int = 0) -> bool:
        if isinstance(xmax_or_map, list):
            xmax = len(xmax_or_map)
            ymax = len(xmax_or_map[0])
        else:
            xmax = xmax_or_map

        return xmin <= self.x < xmax and ymin <= self.y < ymax

    def get(self, map: List[List[T]]) -> T | None:
        assert len(map) > 0, 'Map must have at least one row'
        assert len(map[0]) > 0, 'Map must have at least one column'

        return (
            map[self.x][self.y]
            if 0 <= self.x < len(map)
            and 0 <= self.y < len(map[self.x])
            else None
        )

    def set(self, map: List[List[T]], value: T):
        assert len(map) > 0, 'Map must have at least one row'
        assert len(map[0]) > 0, 'Map must have at least one column'
        assert 0 <= self.x < len(map), 'X is outside the map'
        assert 0 <= self.y < len(map[self.x]), 'Y is outside the map'

        map[self.x][self.y] = value

    def right(self) -> 'Coord':
        return Coord(x=self.x,y=self.y+1)
    def left(self) -> 'Coord':
        return Coord(x=self.x,y=self.y-1)
    def up(self) -> 'Coord':
        return Coord(x=self.x-1,y=self.y)
    def down(self) -> 'Coord':
        return Coord(x=self.x+1,y=self.y)

    def move(self, dir: Direction):
        match dir:
          case 'left':
            return self.left()
          case 'right':
            return self.right()
          case 'up':
            return self.up()
          case 'down':
            return self.down()

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

    @staticmethod
    def all_coords(xmax_or_map: int | List[List[T]], ymax: int = 0, xmin: int = 0, ymin: int = 0) -> Generator['Coord', None, None]:
        if isinstance(xmax_or_map, list):
            xmax = len(xmax_or_map)
            ymax = len(xmax_or_map[0])
        else:
            xmax = xmax_or_map

        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                yield Coord(x=x, y=y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x - other.x, self.y - other.y)

    @property
    def manhatten_distance(self) -> int:
        return abs(self.x) + abs(self.y)
