from typing import *
from solutions2023.lib import *

Row = List[int]
Input = List[Row]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = p.reg(r'[1-9]') > int
  line = p.rep(n)
  input = p.repsep(line, '\n')

class Path(NamedTuple):
  nodes: List[twod.Coord]
  dir: twod.Direction | None
  reps: int # times going that direction
  cost: int

  def _move(self, dir: twod.Direction, costs: List[List[int]], part2: bool) -> Optional['Path']:
    next = self.nodes[-1].move(dir)
    if not next.inbounds(costs):
      return None
    if not part2 and self.reps == 3 and self.dir == dir:
      return None
    if next in self.nodes:
      return None
    if part2 and self.reps < 4 and self.dir is not None and self.dir != dir:
      return None
    if part2 and self.reps == 10 and self.dir == dir:
      return None
    return Path(self.nodes + [next], dir, self.reps + 1 if dir == self.dir else 1, self.cost + next.get(costs))

  def _adj_paths(self, costs: List[List[int]], part2: bool) -> List['Path']:
    match self.dir:
      case 'up':
        return [self._move('right', costs, part2), self._move('left', costs, part2), self._move('up', costs, part2)]
      case 'down':
        return [self._move('right', costs, part2), self._move('left', costs, part2), self._move('down', costs, part2)]
      case 'left':
        return [self._move('up', costs, part2), self._move('down', costs, part2), self._move('left', costs, part2)]
      case 'right':
        return [self._move('up', costs, part2), self._move('down', costs, part2), self._move('right', costs, part2)]
      case None: # only happens on start
        return [self._move('up', costs, part2), self._move('down', costs, part2), self._move('right', costs, part2), self._move('left', costs, part2)]

  def adj_paths(self, costs: List[List[int]], part2: bool = False) -> List['Path']:
    return [p for p in self._adj_paths(costs, part2) if p is not None]

  @property
  def sans_cost(self):
    return (self.nodes[-1], self.dir, self.reps)

  @property
  def last_node(self) -> twod.Coord:
    return self.nodes[-1]

  def __str__(self) -> str:
    return f'(({self.nodes[-1].x}, {self.last_node.y}) [{len(self.nodes)}], {self.dir}x{self.reps}, {self.cost})'

def bfs(costs: List[List[int]], start: twod.Coord, target: twod.Coord, part2: bool = False) -> int:
  discovered: Dict[Tuple[twod.Coord, twod.Direction | None, int], int] = collections.defaultdict(lambda: 100000)
  discovered[(start, None, 1)] = 0

  q = PriorityQueue(key=lambda path: (path.cost, -path.last_node.manhatten_distance))
  q.push(Path([start], None, 1, 0))

  while len(q.q) > 0:
    p = q.pop()
    debug(f'{p.last_node.manhatten_distance} {p.cost} {len(discovered)} ({len(costs)}x{len(costs[0])})')
    for path in p.adj_paths(costs, part2):
      if path.cost < discovered[path.sans_cost]:
        q.push(path)
        discovered[path.sans_cost] = path.cost

  return min(value for path, value in discovered.items() if path[0] == target)


class Day17(Advent[Input]):
    year = 2023
    day = 17

    samples = [
'''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      return bfs(input, twod.Coord(0,0), twod.Coord(len(input)-1, len(input[0])-1))

    def solve2(self, input: Input) -> Any:
      return bfs(input, twod.Coord(0,0), twod.Coord(len(input)-1, len(input[0])-1), part2=True)

if __name__ == '__main__':
    Day17().main()
