from typing import *
from solutions2023.lib import *

class Node(NamedTuple):
  id: str
  left: str
  right: str

Input = Tuple[str, List[Node]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  instructions = p.reg(r'[RL]+')
  node = p.reg(r'[A-Z0-9]{3}')
  connections = p.lit('(') >> p.repsep(node, ',', min=2, max=2) << p.lit(')')
  line = ((node << p.lit('=')) & connections) > (lambda pair: Node(pair[0], *pair[1]))
  input = (instructions << p.lit('\n\n')) & p.repsep(line, '\n')

class Day8(Advent[Input]):
    year = 2023
    day = 8

    samples = [
'''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)''',
'''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)''',
'''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      instructions, nodes = input
      nodemap = {node.id: node for node in nodes}

      cur = 'AAA'
      ptr = 0
      steps = 0

      while cur != 'ZZZ':
        match instructions[ptr]:
          case 'R':
            cur = nodemap[cur].right
          case 'L':
            cur = nodemap[cur].left

        ptr = (ptr + 1) % len(instructions)
        steps += 1

      return steps

    def solve2(self, input: Input) -> Any:
      instructions, nodes = input
      nodemap = {node.id: node for node in nodes}

      def find_zs(node_id, zcount = 10):
        zsteps = []
        cur = node_id
        ptr = 0
        steps = 0

        while len(zsteps) < zcount:
          match instructions[ptr]:
            case 'R':
              cur = nodemap[cur].right
            case 'L':
              cur = nodemap[cur].left

          ptr = (ptr + 1) % len(instructions)
          steps += 1

          if cur.endswith('Z'):
            zsteps += [steps]

        return zsteps

      starts = [node.id for node in nodes if node.id.endswith('A')]
      zss = [find_zs(start) for start in starts]
      diffs = [[y-x for x,y in zip(zs, zs[1:])] for zs in zss]

      for ds in diffs:
        assert all(d == ds[0] for d in ds)

      periods = [ds[0] for ds in diffs]
      return math.lcm(*periods)

if __name__ == '__main__':
    Day8().main()
