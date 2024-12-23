from typing import *
from advent.lib import *
import networkx as nx

Conn = Tuple[str, str]
Input = List[Conn]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  comp = p.reg(r'[a-z]+')
  conn = p.repsep(comp, '-', min=2, max=2) > tuple
  line = conn
  input = p.repsep(line, '\n')

class Day23(Advent[Input]):
    year = 2024
    day = 23

    samples = [
'''
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      # g = nx.Graph()
      # g.add_edges_from(input)
      # for comp in nx.connected_components(g):
      #   print(comp)

      nodes = {n for conn in input for n in conn}
      edges = {
        node: [edge for edge in input if node in edge]
        for node in nodes
      }

      def connected(n: str) -> Set[str]:
        return {
          n2 for edge in edges[n] for n2 in edge if n2 != n
        }

      tnodes = [n for n in nodes if n.startswith('t')]

      trips = [
        tuple(sorted([tnode, n1, n2]))
        for tnode in tnodes
        for n1, n2 in itertools.product(connected(tnode), connected(tnode))
        if n1 != n2 and n1 < n2 and n2 in connected(n1)
      ]

      return len(set(trips))

    def solve2(self, input: Input) -> Any:
      nodes = {n for conn in input for n in conn}
      edges = {
        node: [edge for edge in input if node in edge]
        for node in nodes
      }
      connected = {
        node: {n2 for edge in edges[node] for n2 in edge if n2 != node}
        for node in nodes
      }

      @functools.cache
      def grow(nodes: Tuple[str]) -> Generator[Tuple[str], None, None]:
        others: Set[str] = set()
        for node in nodes:
          if not len(others):
            others = set(connected[node])
          else:
            others = others.intersection(connected[node])

        if len(others):
          while len(others):
            nextother = others.pop()
            for nlist in grow(tuple(sorted(list(nodes) + [nextother]))):
              others = others.difference(nlist)
              yield nlist

        yield nodes

      biggest = max(
        (nlist for edge in tqdm(input) for nlist in grow(tuple(sorted(edge)))),
        key=lambda nset: len(nset)
      )

      return ','.join(sorted(biggest))


if __name__ == '__main__':
    Day23().main()
