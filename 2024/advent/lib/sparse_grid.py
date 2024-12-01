import collections
from typing import *
from . import twod

Coord = TypeVar('Coord')
T = TypeVar('T')
class SparseGrid:
  _g: Dict[Coord, T]
  _default: T

  def __init__(self, default_value: T):
    self._default = default_value
    self._g = collections.defaultdict(lambda: default_value)

  def __getitem__(self, coord: Coord) -> T:
    return self._g[coord]

  def set(self, coord: Coord, v: T):
    if v == self._default:
      del self._g[coord]
    else:
      self._g[coord] = v

  def clear(self, coord: Coord):
      del self._g[coord]

  def twodstr(self, state_to_str: Callable[[T], str]) -> str:
    coords = list(self._g.keys())
    assert len(coords) > 0 and isinstance(coords[0], twod.Coord)

    minx = min(c.x for c in coords)
    maxx = max(c.x for c in coords)
    miny = min(c.y for c in coords)
    maxy = max(c.y for c in coords)
    
    return '\n'.join(
      ''.join(
        state_to_str(self._g[twod.Coord(x,y)])
        for y in range(miny,maxy+1)
      )
      for x in range(minx, maxx+1)
    )
