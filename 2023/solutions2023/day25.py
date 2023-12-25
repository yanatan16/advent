from typing import *
from solutions2023.lib import *

Node = str
Edge = Tuple[Node, Node]
Input = List[Edge]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  node = p.reg(r'[a-z]+')
  line = (node << p.lit(':')) & p.rep(node)
  lines = p.repsep(line, '\n')
  input = lines > (lambda ls: [(a, b) for a, bs in ls for b in bs])

class Day25(Advent[Input]):
    year = 2023
    day = 25

    samples = [
'''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, edges: Input) -> Any:
      g = nx.Graph()
      nodes = {n for edge in edges for n in edge}
      for a, b in edges:
        g.add_edge(a, b, capacity=1)

      # Try 3 edmonds-karp
      for source, target in itertools.combinations(nodes, 2):
        cut, partitions = nx.minimum_cut(g, source, target)
        if cut == 3:
          return len(partitions[0])*len(partitions[1])

      return -1

    def solve2(self, input: Input) -> Any:
        return 'Not implemented'

if __name__ == '__main__':
    Day25().main()
