from typing import *
from dataclasses import dataclass
import math

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

    def right(self, n: int = 1) -> 'Coord':
        return Coord(x=self.x,y=self.y+n)
    def left(self, n: int = 1) -> 'Coord':
        return Coord(x=self.x,y=self.y-n)
    def up(self, n: int = 1) -> 'Coord':
        return Coord(x=self.x-n,y=self.y)
    def down(self, n: int = 1) -> 'Coord':
        return Coord(x=self.x+n,y=self.y)

    def move(self, dir: Direction, n: int = 1):
        match dir:
          case 'left':
            return self.left(n)
          case 'right':
            return self.right(n)
          case 'up':
            return self.up(n)
          case 'down':
            return self.down(n)

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

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x - other.x, self.y - other.y)

    def __neg__(self) -> 'Coord':
        return Coord(-self.x, -self.y)

    @property
    def manhatten_distance(self) -> int:
        return abs(self.x) + abs(self.y)

    def wrap(self, xmax_or_map: int | List[List[T]], ymax: int = 0, xmin: int = 0, ymin: int = 0) -> 'Coord':
        if isinstance(xmax_or_map, list):
            xmax = len(xmax_or_map)
            ymax = len(xmax_or_map[0])
        else:
            xmax = xmax_or_map

        if self.inbounds(xmax, ymax, xmin, ymin):
            return self

        return Coord(
            x=((self.x - xmin) % xmax) + xmin,
            y=((self.y - ymin) % ymax) + ymin,
        )

    def gcd_vector(self) -> 'Coord':
        gcd = math.gcd(abs(self.x), abs(self.y))
        if gcd > 1:
            return Coord(self.x // gcd, self.y // gcd)
        return self



@dataclass
class Edge:
  start: Coord
  end: Coord

  def __len__(self) -> int:
      if self.start.x == self.end.x:
          return abs(self.start.y - self.end.y)
      else:
          return abs(self.start.x - self.end.x)

  def contains(self, c: Coord) -> bool:
    if self.start.x == self.end.x:
      return c.x == self.start.x and min(self.start.y, self.end.y) <= c.y <= max(self.start.y, self.end.y)
    else:
      return c.y == self.start.y and min(self.start.x, self.end.x) <= c.x <= max(self.start.x, self.end.x)

  @staticmethod
  def area(edges: List['Edge']) -> int:
      inner_area = int(abs(sum(
          (edge.start.x - edge.end.x) * (edge.start.y + edge.end.y) / 2
          for edge in edges
      )))
      outer_area = int(Edge.circumference(edges) / 2 + 1)

      return inner_area + outer_area

  @staticmethod
  def circumference(edges: List['Edge']) -> int:
      return sum(len(e) for e in edges)
