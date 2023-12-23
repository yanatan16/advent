from typing import *
from solutions2023.lib import *

Input = List[str]
Coord = twod.Coord

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#><^v]+')
  n = UtilityParsers.integer
  line = n
  input = p.repsep(mapline, '\n')

def find_longest_path(forest: Input, start: Coord, target: Coord, path: List[Coord], part2: bool = False) -> int | None:
  cur = start
  length = 1

  while cur != target:
    # debug(f'find_longest_path {", ".join(map(str, path))} -> {cur}')
    if cur in path:
      return None

    path = path + [cur]

    if cur.get(forest) == '>' and not part2:
      cur = cur.right()
    elif cur.get(forest) == '<' and not part2:
      cur = cur.left()
    elif cur.get(forest) == '^' and not part2:
      cur = cur.up()
    elif cur.get(forest) == 'v' and not part2:
      cur = cur.down()
    else:
      poss = [n for n in cur.neighbors() if n.inbounds(forest) and n not in path and n.get(forest) != '#']

      if len(poss) == 0:
        return None # Failed path
      elif len(poss) == 1:
        cur = poss[0]
      else:
        subpaths = [find_longest_path(forest, n, target, path, part2) for n in poss]
        if all(p is None for p in subpaths):
          return None

        return max((p for p in subpaths if p is not None), key=lambda p: len(p))

  return path

Node = Coord
class Edge(NamedTuple):
  nodes: Tuple[Node, Node]
  weight: int

@dataclass
class Graph:
  nodes: List[Node]
  edges: List[Edge]

  def edgelookup(self) -> Dict[Node, List[Tuple[Node, int]]]:
    edgetupes = [t for (a, b), weight in self.edges for t in [(a, b, weight), (b, a, weight)]]
    edgetupes.sort(key=lambda t: t[0])
    edgegrps = itertools.groupby(edgetupes, key=lambda t: t[0])
    return {
      node: [(b, weight) for _, b, weight in grp]
      for node, grp in edgegrps
    }

  def longest_path(self, path: List[Node], target: Node, total_weight: int = 0) -> Tuple[int, List[Node]] | None:
    edgelookup = self.edgelookup()

    start = path[-1]
    if start == target:
      return total_weight, path

    valid_edges = [
      (b, weight)
      for b, weight in edgelookup.get(start, [])
      if b not in path
    ]

    paths = [self.longest_path(path + [b], target, total_weight + weight) for b, weight in valid_edges]
    valid_paths = [path for path in paths if path is not None]

    return max(valid_paths) if valid_paths else None



class Day23(Advent[Input]):
    year = 2023
    day = 23

    samples = [
'''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      start = Coord(0, 1)
      target = Coord(len(input)-1, len(input[0])-2)
      forest = input

      path = find_longest_path(forest, start, target, [])


      debug('\n'.join(
        ''.join('S' if Coord(i,j) == start else 'O' if Coord(i,j) in path else Coord(i,j).get(forest)
                for j in range(len(forest[0])))
        for i in range(len(forest))
      ))
      debug(', '.join(str(c) for c in path))
      return len(path)

    def solve2(self, input: Input) -> Any:
      points = [c for c in Coord.all_coords(input) if c.get(input) != "#"]

      choices = [
        c for c in points
        if len([n for n in c.neighbors()
                if n.get(input) != "#"
                and n.inbounds(input)]) > 2
      ]
      start = Coord(0, 1)
      target = Coord(len(input)-1, len(input[0])-2)
      nodes = [start, target] + choices

      def walk_edge(node: Coord, neighbor: Coord) -> None | Edge:
        path = [node, neighbor]
        while path[-1] not in nodes:
          nxts = [n for n in path[-1].neighbors() if n not in path and n.get(input) != '#' and n.inbounds(input)]
          if len(nxts) == 0:
            return None
          elif len(nxts) == 1:
            path += [nxts[0]]
          else:
            raise ValueError(f'Found multiple options at non-node {path}: {nxts}')

        # sort so they can be uniqued
        a, b = sorted([node, path[-1]])

        return Edge(nodes=(a, b), weight=len(path) - 1)

      edges = {
        walk_edge(node, neighbor)
        for node in nodes
        for neighbor in node.neighbors()
        if neighbor.get(input) != '#'
        and neighbor.inbounds(input)
      }

      print(f'Reduced {len(input)}x{len(input[0])} forest down to {len(nodes)} nodes with {len(edges)} edges')
      g = Graph(nodes=nodes, edges=list(edges))

      weight, path = g.longest_path([start], target)
      print(f'Path: {path}')
      return weight


if __name__ == '__main__':
    Day23().main()
